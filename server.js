// server.js
const express = require("express");
const fs = require("fs");
const path = require("path");
const ExcelJS = require("exceljs"); // <-- Tambah exceljs
const app = express();

app.use(express.json());

// === Load mapping dari tag.json ===
const mappingPath = path.join(__dirname, "tag.json");
let tagMapping = {};

try {
  const data = fs.readFileSync(mappingPath, "utf-8");
  tagMapping = JSON.parse(data);
  console.log("✅ Mapping loaded:", Object.keys(tagMapping).length, "tags");
} catch (err) {
  console.error("❌ Failed to load tag.json:", err);
  process.exit(1);
}

// Buat reverse map: tagValue → tagKey
const reverseMap = {};
for (const [key, value] of Object.entries(tagMapping)) {
  reverseMap[value] = key;
}

// === Tempat simpan tag yang sudah pernah terdeteksi ===
const detectedSet = new Set();

// === Route untuk menerima RFID batch ===
app.post("/rfid", (req, res) => {
  const data = req.body;

  if (!data || Object.keys(data).length === 0) {
    return res.status(400).json({ error: "Invalid JSON" });
  }

  if (data.api_result) {
    console.log("\n📡 API RESULT RECEIVED");
    return res.status(200).json({ message: "API result received" });
  }

  // === Cek tag batch ===
  const batchTags = data.idHex || [];
  console.log("\n[INFO] Received tag batch:");
  console.log(data);

  const detectedNow = [];
  const unknown = [];

  // Simpan tag baru yang masuk
  for (const tag of batchTags) {
    if (reverseMap[tag]) {
      detectedSet.add(tag); // simpan kumulatif
      detectedNow.push({ tag, key: reverseMap[tag] });
    } else {
      unknown.push(tag);
    }
  }

  // Buat list semua detected kumulatif
  const detectedAll = Array.from(detectedSet).map((tag) => ({
    tag,
    key: reverseMap[tag] || null,
  }));

  // Cari yang masih hilang (belum pernah terdeteksi sama sekali)
  const missing = [];
  for (const [key, value] of Object.entries(tagMapping)) {
    if (!detectedSet.has(value)) {
      missing.push({ key, tag: value });
    }
  }

  // Log hasil
  console.log("✅ Detected (this batch):");
  console.table(detectedNow);

  if (unknown.length > 0) {
    console.log("⚠️ Unknown tags (tidak ada di mapping):");
    console.table(unknown);
  }

  console.log("📌 Total detected so far:");
  console.table(detectedAll);

  console.log("❌ Missing tags:");
  console.table(missing);

  return res.status(200).json({
    message: "Batch processed",
    detectedNow,
    detectedAll,
    unknown,
    missing,
  });
});

// === Endpoint untuk reset memory ===
app.post("/reset", (req, res) => {
  detectedSet.clear();
  console.log("🔄 Detected set has been reset.");
  res.json({ message: "Detected tags reset" });
});

// === Endpoint export hasil ke Excel ===
app.get("/export", async (req, res) => {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet("RFID Scan Result");

  // Header
  worksheet.columns = [
    { header: "Key", key: "key", width: 20 },
    { header: "Tag ID", key: "tag", width: 40 },
  ];

  // Isi data: kalau sudah terdeteksi → isi Tag, kalau belum → kosong
  for (const [key, value] of Object.entries(tagMapping)) {
    worksheet.addRow({
      key,
      tag: detectedSet.has(value) ? value : "",
    });
  }

  // Simpan file sementara
  const filePath = path.join(__dirname, "scan_result.xlsx");
  await workbook.xlsx.writeFile(filePath);

  console.log("📤 Exported scan_result.xlsx");

  res.download(filePath, "scan_result.xlsx", (err) => {
    if (err) console.error("❌ Error sending file:", err);
  });
});

// Jalankan server
const PORT = 5000;
app.listen(PORT, "0.0.0.0", () => {
  console.log(`🚀 Server running on http://0.0.0.0:${PORT}`);
});
