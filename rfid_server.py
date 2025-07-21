from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/rfid', methods=['POST'])
def receive_data():
    # print("== NEW REQUEST ==")
    # print("Headers:")
    # for key, value in request.headers.items():
    #     print(f"{key}: {value}")

    try:
        data = request.get_json(force=True)
    except Exception as e:
        print(f"\nERROR: Failed to parse JSON - {e}")
        return jsonify({"error": "Invalid JSON format"}), 400

    print("=========================")
    print("Received JSON:")
    print(data)
    print("=========================")

    # === VALIDASI STRUKTUR ===
    required_keys = ["reader_id", "antenna", "idHex", "timestamp"]
    if not all(k in data for k in required_keys):
        print("ERROR: Missing one or more required keys.")
        return jsonify({"error": "Missing required fields"}), 400

    # print("\nParsed fields:")
    print(f"Reader ID : {data['reader_id']}")
    print(f"Antenna   : {data['antenna']}")
    print(f"Tag ID    : {data['idHex']}")
    print(f"Timestamp : {data['timestamp']}")

    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
