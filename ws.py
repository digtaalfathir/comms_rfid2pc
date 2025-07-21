import websocket
import ssl
import json
import threading

# Konfigurasi
READER_WS_URL = "wss://192.168.123.10:443"  # atau "ws://" jika tidak pakai SSL
VERIFY_CERT = False  # Jika pakai sertifikat self-signed

# Fungsi callback untuk menangani pesan masuk
def on_message(ws, message):
    try:
        data = json.loads(message)
        print("✅ Data diterima:", json.dumps(data, indent=2))
    except Exception as e:
        print("❌ Gagal parse message:", str(e))

# Callback saat koneksi dibuka
def on_open(ws):
    print("🔗 Koneksi WebSocket berhasil dibuka")

# Callback saat koneksi ditutup
def on_close(ws, close_status_code, close_msg):
    print("🔌 Koneksi WebSocket ditutup:", close_status_code, close_msg)

# Callback jika error
def on_error(ws, error):
    print("⚠️ Error WebSocket:", error)

# Jalankan WebSocket Client
def run_ws():
    ws = websocket.WebSocketApp(
        READER_WS_URL,
        on_message=on_message,
        on_open=on_open,
        on_close=on_close,
        on_error=on_error
    )

    if READER_WS_URL.startswith("wss://"):
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE if not VERIFY_CERT else ssl.CERT_REQUIRED})
    else:
        ws.run_forever()

if __name__ == "__main__":
    threading.Thread(target=run_ws).start()
