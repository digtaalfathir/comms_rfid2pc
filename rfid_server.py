from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/rfid', methods=['POST'])
def handle_rfid():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    if 'api_result' in data:
        result = data['api_result']
        print("\n=== API RESULT RECEIVED ===")

        if 'status' in result:
            print(f"[SUCCESS] Status: {result['status']}")
            print(f"Response: {result['response']}")
        elif 'error' in result:
            print(f"[ERROR] {result['error']}")

        print(f"Original Payload: {result.get('original_payload', {})}")
        print("===========================\n")
        return jsonify({"message": "API result received"}), 200

    else:
        # Ini kemungkinan data batch biasa, bukan feedback dari API
        print("\n[INFO] Received tag batch:")
        print(data)
        return jsonify({"message": "Batch data received"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
