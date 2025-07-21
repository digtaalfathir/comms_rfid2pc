# file: log_listener.py
import socket

HOST = "0.0.0.0"   # Dengarkan semua interface
PORT = 40514       # Sesuai dengan DEBUG_PORT plugin kamu

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[Logger] Menunggu koneksi log di port {PORT}...")
    conn, addr = s.accept()
    with conn:
        print(f"[Logger] Terhubung dari {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data.decode("utf-8").strip())
