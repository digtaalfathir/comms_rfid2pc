import pandas as pd
import json

# Buka file Excel
file_path = "tag.xlsx"  # ganti dengan nama filemu
xls = pd.ExcelFile(file_path)

result = {}

# Loop setiap sheet
for sheet_index, sheet_name in enumerate(xls.sheet_names, start=1):
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
    
    # Ambil semua kolom
    for row_index, row in df.iterrows():
        for col in df.columns:
            key = f"M{sheet_index}-{col}-{row_index+1}"  # row_index+1 biar mulai dari 1
            value = row[col]
            
            if pd.notna(value):  # hanya simpan yang tidak kosong
                result[key] = str(value)

# Simpan ke file JSON
with open("tag.json", "w") as f:
    json.dump(result, f, indent=2)
