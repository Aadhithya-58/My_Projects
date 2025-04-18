from flask import Flask, jsonify, request
from flask_cors import CORS
import serial
import firebase_admin
from firebase_admin import credentials, db
import datetime

app = Flask(__name__)
CORS(app)

# Local storage
scanned_products = []

# Serial Port Configuration
SERIAL_PORT = "COM6"  # Adjust as needed
BAUD_RATE = 115200

# Firebase Initialization
cred = credentials.Certificate("C:/Users/admin/Downloads/cloud_firebase/serviceaccountkey.json")  # Adjust path
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://cloud-integration-c6dde-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

firebase_ref = db.reference("scanned_products")
registered_users_ref = db.reference("registered_users")  # Add reference to registered users

@app.route('/scan-product', methods=['GET'])
def scan_product():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            qr_data = ser.readline().decode('utf-8').strip()
            print("✅ Scanned product:", qr_data)

            if qr_data:
                timestamp = datetime.datetime.now().isoformat()

                # Get the active user from the request (dynamic)
                active_user_id = request.args.get('user_id')

                # Basic validation: ensure user_id is provided.
                if not active_user_id:
                  return jsonify({"success": False, "message": "user_id is required"}), 400

                # Basic Validation: check user exists
                users = registered_users_ref.get() or {}
                if active_user_id not in users:
                    return jsonify({"success": False, "message": "User not found"}), 404

                product_entry = {
                    "id": len(scanned_products) + 1,
                    "product": qr_data,
                    "timestamp": timestamp,
                    "scannedBy": active_user_id, #ADDED THIS LINE
                }

                # Save locally
                scanned_products.append(product_entry)

                # Push to Firebase using the product as the key
                firebase_ref.child(qr_data).set(product_entry)

                return jsonify({
                    "success": True,
                    "product": qr_data,
                    "message": "Product scanned and saved!"
                })
            else:
                return jsonify({
                    "success": False,
                    "message": "No data scanned"
                }), 400

    except serial.SerialException as se:
        print("❌ Serial Error:", se)
        return jsonify({
            "success": False,
            "error": "Serial port error",
            "message": str(se)
        }), 500
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/get-scanned-products', methods=['GET'])
def get_products():
    return jsonify({"products": scanned_products})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

"""from flask import Flask, jsonify
from flask_cors import CORS
import serial
import firebase_admin
from firebase_admin import credentials, db
import datetime

app = Flask(__name__)
CORS(app)

# Local storage
scanned_products = []

# Serial Port Configuration
SERIAL_PORT = "COM6"
BAUD_RATE = 115200

# Firebase Initialization
cred = credentials.Certificate("C:/Users/admin/Downloads/cloud_firebase/serviceaccountkey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://cloud-integration-c6dde-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

firebase_ref = db.reference("scanned_products")

@app.route('/scan-product', methods=['GET'])
def scan_product():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            qr_data = ser.readline().decode('utf-8').strip()
            print("✅ Scanned product:", qr_data)

            if qr_data:
                timestamp = datetime.datetime.now().isoformat()
                product_entry = {
                    "id": len(scanned_products) + 1,
                    "product": qr_data,
                    "timestamp": timestamp
                }

                # Save locally
                scanned_products.append(product_entry)

                # Push to Firebase using the product as the key
                firebase_ref.child(qr_data).set(product_entry)  # Changed from push() to set()

                return jsonify({
                    "success": True,
                    "product": qr_data,
                    "message": "Product scanned and saved!"
                })
            else:
                return jsonify({
                    "success": False,
                    "message": "No data scanned"
                }), 400

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/get-scanned-products', methods=['GET'])
def get_products():
    return jsonify({"products": scanned_products})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
"""