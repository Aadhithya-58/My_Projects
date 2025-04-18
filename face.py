import os
import cv2
import numpy as np
import face_recognition
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import requests

app = Flask(__name__)
CORS(app)
cred = credentials.Certificate("C:/Users/admin/Downloads/cloud_firebase/serviceaccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cloud-integration-c6dde-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

KNOWN_FACES_DIR = "known_faces"
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

def is_face_already_registered(new_face_img):
    for filename in os.listdir(KNOWN_FACES_DIR):
        existing_img_path = os.path.join(KNOWN_FACES_DIR, filename)
        existing_img = face_recognition.load_image_file(existing_img_path)
        existing_encoding = face_recognition.face_encodings(existing_img)
        new_encoding = face_recognition.face_encodings(new_face_img)
        
        if existing_encoding and new_encoding:
            match = face_recognition.compare_faces([existing_encoding[0]], new_encoding[0])
            if match[0]:
                return filename.split(".")[0]  # Return existing name
    return None

@app.route('/register_face', methods=['POST'])
def register_face():
    data = request.json
    name = data.get('name')
    img_data = data.get('image')
    if not name or not img_data:
        return jsonify({"error": "Name and image are required"}), 400

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_img)

    if len(face_encodings) == 0:
        return jsonify({"error": "No face detected"}), 400
    elif len(face_encodings) > 1:
        return jsonify({"error": "Multiple faces detected. Register only one person at a time."}), 400
    
    existing_user = is_face_already_registered(rgb_img)
    if existing_user:
        return jsonify({"error": f"User already registered as {existing_user}"}), 400

    img_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
    cv2.imwrite(img_path, img)
    return jsonify({"message": f"User {name} registered successfully! Now tap your RFID card."})

@app.route('/register_rfid', methods=['POST'])
def register_rfid():
    data = request.json
    name = data.get('name')
    rfid = data.get('rfid')
    if not name or not rfid:
        return jsonify({"error": "Name and RFID are required"}), 400

    ref = db.reference("registered_users")
    ref.child(name).set({"name": name, "rfid": rfid})  # Store as an object
    return jsonify({"message": f"RFID {rfid} registered successfully for {name}."})


@app.route('/identify', methods=['POST'])
def identify():
    data = request.json
    img_data = data.get('image')
    if not img_data:
        return jsonify({"error": "Image is required"}), 400

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_img)

    if len(face_encodings) == 0:
        return jsonify({"error": "No face detected"}), 400
    elif len(face_encodings) > 1:
        return jsonify({"error": "Multiple faces detected. Please try again with only one person."}), 400

    ref = db.reference("registered_users")
    registered_users = ref.get() or {}

    match_name = "Unknown"
    for filename in os.listdir(KNOWN_FACES_DIR):
        existing_img_path = os.path.join(KNOWN_FACES_DIR, filename)
        existing_img = face_recognition.load_image_file(existing_img_path)
        existing_encoding = face_recognition.face_encodings(existing_img)
        
        if existing_encoding:
            match = face_recognition.compare_faces([existing_encoding[0]], face_encodings[0])
            if match[0]:
                match_name = filename.split(".")[0]  # Extract name from filename
                rfid = registered_users.get(match_name, "RFID not found")
                return jsonify({"identity": match_name, "rfid": rfid})

    return jsonify({"error": "Face recognized but RFID not found. Please scan RFID first."}), 400

ESP32_IP = "172.31.250.32"

@app.route('/get_rfid', methods=['GET'])
def get_rfid():
    try:
        response = requests.get(f"http://{ESP32_IP}/rfid")
        response.raise_for_status()
        data = response.json()
        if "rfid" in data:
            return jsonify({"rfid": data["rfid"]})
        return jsonify({"error": "No RFID data received"}), 500
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

#PRE-FINAL-CODE
"""import os
import cv2
import numpy as np
import face_recognition
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import requests

app = Flask(__name__)
CORS(app)
cred = credentials.Certificate("C:/Users/admin/Downloads/cloud_firebase/serviceaccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cloud-integration-c6dde-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

KNOWN_FACES_DIR = "known_faces"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

def load_known_faces():
    known_faces = {}
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith(".jpg"):
            name = os.path.splitext(filename)[0]
            img_path = os.path.join(KNOWN_FACES_DIR, filename)
            img = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(img)
            if encoding:
                known_faces[name] = encoding[0]
    return known_faces

known_faces = load_known_faces()

@app.route('/register_face', methods=['POST'])
def register_face():
    data = request.json
    name = data.get('name')
    img_data = data.get('image')
    if not name or not img_data:
        return jsonify({"error": "Name and image are required"}), 400

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
    cv2.imwrite(img_path, img)  # Save image to disk
    
    global known_faces
    known_faces = load_known_faces()  # Reload known faces
    return jsonify({"message": f"User {name} registered successfully! Now tap your RFID card."})

@app.route('/register_rfid', methods=['POST'])
def register_rfid():
    data = request.json
    name = data.get('name')
    rfid = data.get('rfid')
    if not name or not rfid:
        return jsonify({"error": "Name and RFID are required"}), 400

    ref = db.reference("registered_users")
    ref.child(name).set({"rfid": rfid})  # Store in name: {rfid} format
    return jsonify({"message": f"RFID {rfid} registered successfully for {name}."})

@app.route('/identify', methods=['POST'])
def identify():
    data = request.json
    img_data = data.get('image')
    if not img_data:
        return jsonify({"error": "Image is required"}), 400

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_img)

    if len(face_encodings) == 0:
        return jsonify({"error": "No face detected"}), 400

    ref = db.reference("registered_users")
    registered_users = ref.get() or {}

    match_name = "Unknown"
    for name, encoding in known_faces.items():
        matches = face_recognition.compare_faces([encoding], face_encodings[0])
        if matches[0]:
            if name in registered_users:
                return jsonify({"identity": name, "rfid": registered_users[name]["rfid"]})
            return jsonify({"error": "Face recognized but RFID not found. Please scan RFID first."}), 400
    
    return jsonify({"error": "Unauthorized User: Face not registered"}), 403

ESP32_IP = "192.168.162.32"

@app.route('/get_rfid', methods=['GET'])
def get_rfid():
    try:
        response = requests.get(f"http://{ESP32_IP}/rfid", timeout=5)
        response.raise_for_status()
        data = response.json()
        if "rfid" in data:
            return jsonify({"rfid": data["rfid"]})
        return jsonify({"error": "No RFID data received"}), 500
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
"""
#MOST_RECENT_ONE
"""import os
import cv2
import numpy as np
import face_recognition
import base64
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import requests

app = Flask(__name__)
CORS(app)
cred = credentials.Certificate("C:/Users/admin/Downloads/cloud_firebase/serviceaccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cloud-integration-c6dde-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

KNOWN_FACES_DIR = "known_faces"
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

encodings_file = "face_encodings.pkl"
if os.path.exists(encodings_file):
    with open(encodings_file, "rb") as f:
        known_faces = pickle.load(f)
else:
    known_faces = {}

def save_encodings():
    with open(encodings_file, "wb") as f:
        pickle.dump(known_faces, f)

@app.route('/register_face', methods=['POST'])
def register_face():
    data = request.json
    name = data.get('name')
    img_data = data.get('image')
    if not name or not img_data:
        return jsonify({"error": "Name and image are required"}), 400

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_img)

    if len(face_encodings) == 0:
        return jsonify({"error": "No face detected"}), 400

    known_faces[name] = face_encodings[0]
    save_encodings()

    return jsonify({"message": f"User {name} registered successfully! Now tap your RFID card."})

@app.route('/register_rfid', methods=['POST'])
def register_rfid():
    data = request.json
    name = data.get('name')
    rfid = data.get('rfid')
    if not name or not rfid:
        return jsonify({"error": "Name and RFID are required"}), 400

    ref = db.reference("registered_users")
    ref.child(name).set({"rfid": rfid})  # Store in name: {rfid}
    return jsonify({"message": f"RFID {rfid} registered successfully for {name}."})

@app.route('/identify', methods=['POST'])
def identify():
    data = request.json
    img_data = data.get('image')
    if not img_data:
        return jsonify({"error": "Image is required"}), 400

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_img)

    if len(face_encodings) == 0:
        return jsonify({"message": "No face detected"}), 400

    ref = db.reference("registered_users")
    registered_users = ref.get() or {}

    for name, data in registered_users.items():
        if name in known_faces:
            matches = face_recognition.compare_faces([known_faces[name]], face_encodings[0])
            if matches[0]:
                if "rfid" in data:
                    return jsonify({"identity": name, "rfid": data["rfid"]})
                else:
                    return jsonify({"error": "Face recognized but RFID not found. Please scan RFID first."}), 400
    
    return jsonify({"error": "Unauthorized User: Face not registered"}), 403

ESP32_IP = "192.168.162.32"

@app.route('/get_rfid', methods=['GET'])
def get_rfid():
    try:
        response = requests.get(f"http://{ESP32_IP}/rfid", timeout=5)
        response.raise_for_status()
        data = response.json()
        if "rfid" in data:
            return jsonify({"rfid": data["rfid"]})
        return jsonify({"error": "No RFID data received"}), 500
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

"""

#MOST-RECENT-CODE
"""import os
import cv2
import numpy as np
import face_recognition
import base64
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import time
import requests

app = Flask(__name__)
CORS(app)
cred = credentials.Certificate("C:/Users/admin/Downloads/cloud_firebase/serviceaccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cloud-integration-c6dde-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

KNOWN_FACES_DIR = "known_faces"
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

encodings_file = "face_encodings.pkl"
if os.path.exists(encodings_file):
    with open(encodings_file, "rb") as f:
        known_faces = pickle.load(f)
else:
    known_faces = {}

def save_encodings():
    with open(encodings_file, "wb") as f:
        pickle.dump(known_faces, f)

@app.route('/register_face', methods=['POST'])
def register_face():
    data = request.json
    name = data.get('name')
    img_data = data.get('image')
    if not name or not img_data:
        return jsonify({"error": "Name and image are required"}), 400

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_img)

    if len(face_encodings) == 0:
        return jsonify({"error": "No face detected"}), 400

    known_faces[name] = face_encodings[0]
    save_encodings()
    return jsonify({"message": f"User {name} registered successfully! Now tap your RFID card."})

@app.route('/register_rfid', methods=['POST'])
def register_rfid():
    data = request.json
    name = data.get('name')
    rfid = data.get('rfid')
    if not name or not rfid:
        return jsonify({"error": "Name and RFID are required"}), 400

    ref = db.reference("registered_users")
    ref.child(name).set(rfid)  # Store in name:rfid format
    return jsonify({"message": f"RFID {rfid} registered successfully for {name}."})

@app.route('/identify', methods=['POST'])
def identify():
    data = request.json
    img_data = data.get('image')
    if not img_data:
        return jsonify({"error": "Image is required"}), 400

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_img)

    if len(face_encodings) == 0:
        return jsonify({"message": "No face detected"}), 400

    ref = db.reference("registered_users")
    registered_users = ref.get() or {}

    match_name = "Unknown"
    for name, rfid in registered_users.items():
        if name in known_faces:
            matches = face_recognition.compare_faces([known_faces[name]], face_encodings[0])
            if matches[0]:
                match_name = name
                return jsonify({"identity": match_name, "rfid": rfid})
    
    return jsonify({"error": "Face recognized but RFID not found. Please scan RFID first."}), 400

ESP32_IP = "192.168.162.32"

@app.route('/get_rfid', methods=['GET'])
def get_rfid():
    try:
        response = requests.get(f"http://{ESP32_IP}/rfid", timeout=5)
        response.raise_for_status()
        data = response.json()
        if "rfid" in data:
            return jsonify({"rfid": data["rfid"]})
        return jsonify({"error": "No RFID data received"}), 500
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

"""
#RECENT-CODE
"""import os
import cv2
import numpy as np
import face_recognition
import base64
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import time
import requests

app = Flask(__name__)
CORS(app)
cred = credentials.Certificate("C:/Users/admin/Downloads/cloud_firebase/serviceaccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cloud-integration-c6dde-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

KNOWN_FACES_DIR = "known_faces"
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

encodings_file = "face_encodings.pkl"
if os.path.exists(encodings_file):
    with open(encodings_file, "rb") as f:
        known_faces = pickle.load(f)
else:
    known_faces = {}

def save_encodings():
    with open(encodings_file, "wb") as f:
        pickle.dump(known_faces, f)

@app.route('/register_face', methods=['POST'])
def register_face():
    data = request.json
    name = data.get('name')
    img_data = data.get('image')
    if not name or not img_data:
        return jsonify({"error": "Name and image are required"}), 400

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_img)

    if len(face_encodings) == 0:
        return jsonify({"error": "No face detected"}), 400

    if name in known_faces:
        del known_faces[name]

    known_faces[name] = face_encodings[0]
    save_encodings()
    ref = db.reference("registered_faces")
    ref.child(name).set(face_encodings[0].tolist())
    return jsonify({"message": f"User {name} registered successfully! Now tap your RFID card."})

@app.route('/register_rfid', methods=['POST'])
def register_rfid():
    data = request.json
    name = data.get('name')
    rfid = data.get('rfid')
    if not name or not rfid:
        return jsonify({"error": "Name and RFID are required"}), 400

    ref = db.reference("registered_rfids")
    ref.child(name).set({"rfid": rfid, "timestamp": time.time()})
    return jsonify({"message": f"RFID {rfid} registered successfully for {name}. Now you can proceed with face identification."})

@app.route('/identify', methods=['POST'])
def identify():
    data = request.json
    img_data = data.get('image')
    if not img_data:
        return jsonify({"error": "Image is required"}), 400

    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_img)

    if len(face_encodings) == 0:
        return jsonify({"message": "No face detected"}), 400

    ref = db.reference("registered_faces")
    registered_faces = ref.get() or {}
    known_faces = {name: np.array(encoding) for name, encoding in registered_faces.items()}

    match_name = "Unknown"
    for name, encoding in known_faces.items():
        matches = face_recognition.compare_faces([encoding], face_encodings[0])
        if matches[0]:
            match_name = name
            break

    ref = db.reference("registered_rfids")
    registered_rfids = ref.get() or {}

    if match_name in registered_rfids:
        ref = db.reference("identified_faces")
        ref.push({"name": match_name, "timestamp": time.time()})
        return jsonify({"identity": match_name})
    else:
        return jsonify({"error": "Face recognized but RFID not found. Please scan RFID first."}), 400
ESP32_IP = "192.168.162.32"  # Update this IP

@app.route('/get_rfid', methods=['GET'])
def get_rfid():
    try:
        response = requests.get(f"http://{ESP32_IP}/rfid", timeout=5)
        response.raise_for_status()
        data = response.json()
        if "rfid" in data:
            db.reference("scanned_rfids").push({"rfid": data["rfid"], "timestamp": time.time()})
            return jsonify({"rfid": data["rfid"]})
        return jsonify({"error": "No RFID data received"}), 500
    except requests.ConnectionError:
        return jsonify({"error": "ESP32 is unreachable. Check its WiFi connection."}), 500
    except requests.Timeout:
        return jsonify({"error": "ESP32 request timed out. Try again."}), 500
    except requests.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
"""

#OLD-CODE: Use in case of emergency only
"""import os
import cv2
import numpy as np
import face_recognition
import base64
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials,db
import time
app = Flask(__name__)
CORS(app)
cred = credentials.Certificate("C:/Users/admin/Downloads/cloud_firebase/serviceaccountKey.json")  # Replace with your Firebase credentials
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cloud-integration-c6dde-default-rtdb.asia-southeast1.firebasedatabase.app/'  # Replace with your Firebase database URL
})
# Directory to store known faces
KNOWN_FACES_DIR = "known_faces"
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

# Load stored face encodings
encodings_file = "face_encodings.pkl"
if os.path.exists(encodings_file):
    with open(encodings_file, "rb") as f:
        known_faces = pickle.load(f)
else:
    known_faces = {}

def save_encodings():
    #Save known faces to a file.
    with open(encodings_file, "wb") as f:
        pickle.dump(known_faces, f)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    img_data = data.get('image')

    if not name or not img_data:
        return jsonify({"error": "Name and image are required"}), 400

    # Decode base64 image
    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Detect face encodings
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_img)

    if len(face_encodings) == 0:
        return jsonify({"error": "No face detected"}), 400

    # Remove previous entries of the same person
    if name in known_faces:
        del known_faces[name]  # Remove old encoding

    # Save new face encoding
    known_faces[name] = face_encodings[0]
    save_encodings()
    register_face_data(name, face_encodings[0])  # Store in Firebase
    return jsonify({"message": f"User {name} registered successfully!"})

def register_face_data(name, face_encoding):
    global known_faces  # Make sure we're updating the global dictionary
    ref = db.reference("registered_faces")

    try:
        # ❗ Delete old records from Firebase
        for key in (ref.get() or {}).keys():
            if key != name:
                ref.child(key).delete()
        
        # ❗ Clear `known_faces` and add only the new face
        known_faces = {name: face_encoding}
        save_encodings()  # Save updated data locally

        # Store new face encoding in Firebase
        ref.child(name).set(face_encoding.tolist())
        print(f"Face registered successfully for: {name}")

    except Exception as e:
        print(f"Error registering face: {e}")

@app.route('/identify', methods=['POST'])
# Example usage
#store_face_data("Aadhithya", "encoded_data_here")

def identify():
    data = request.json
    img_data = data.get('image')

    if not img_data:
        return jsonify({"error": "Image is required"}), 400

    # Decode base64 image
    img_data = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Detect face encodings
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_img)

    if len(face_encodings) == 0:
        return jsonify({"message": "No face detected"}), 400

    # ❗ Load registered faces from Firebase
    ref = db.reference("registered_faces")
    registered_faces = ref.get() or {}
    
    known_faces = {}
    for name, encoding in registered_faces.items():
        known_faces[name] = np.array(encoding)

    # Compare with known faces
    match_name = "Unknown"
    for name, encoding in known_faces.items():
        matches = face_recognition.compare_faces([encoding], face_encodings[0])
        if matches[0]:
            match_name = name
            break

    # ❗ Save identified face to Firebase
    try:
        ref = db.reference("identified_faces")  # Create new node for identified faces
        ref.push({"name": match_name, "timestamp": time.time()})  # Save with timestamp
        print(f"Identified and stored: {match_name}")
    except Exception as e:
        print(f"Error saving identified face: {e}")

    return jsonify({"identity": match_name})


def store_face_data(name, encoding):
    ref = db.reference("recognized_faces")
    ref.child(name).set({"encoding": encoding})
    print(f"Data sent to Firebase: {name}")  # Debugging print

if __name__ == '__main__':
    app.run(debug=True)"
    """