from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'\x88\xb7\xf7Sa\xf7\x83\xde\x9cv\x1dc\x9d&\x01\xfb>\xc0\x1ar\xc0b\xf1\x15'

# Enable CORS to allow requests from frontend (localhost:3000)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["bloodbridge"]
users_collection = db["users"]
requests_collection = db["requests"]
inventory_collection = db["inventory"]
donors_collection = db["donors"]
events_collection = db["events"]

# Route for account creation
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    users_collection.insert_one({
        "username": data["username"],
        "password": hashed_password,
        "role": data.get("role", "user")  # Default role is 'user'; can be 'admin' or 'hospital'
    })
    return jsonify({"status": "success", "message": "Account created"}), 201

# Route for login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = users_collection.find_one({"username": data["username"]})
    if user and check_password_hash(user["password"], data["password"]):
        session["user"] = user["username"]
        session["role"] = user["role"]
        return jsonify({"status": "success", "role": user["role"], "message": "Login successful"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

# Route for logout
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop("user", None)
    session.pop("role", None)
    return jsonify({"status": "success", "message": "Logged out"}), 200

# Route to get donor management details
@app.route('/api/donor-management', methods=['GET'])
def get_donor_management():
    donor_data = donors_collection.find_one({"username": session.get("user")}, {"_id": 0})
    if donor_data:
        return jsonify(donor_data), 200
    else:
        return jsonify({"error": "Donor data not found"}), 404

# Route for submitting an emergency blood request
@app.route('/api/emergency-request', methods=['POST'])
def emergency_request():
    data = request.json
    blood_type = data.get("bloodType")
    quantity = data.get("quantity")

    # Validate data
    if not blood_type or not quantity:
        return jsonify({"error": "Blood type and quantity are required"}), 400

    # Insert request into the database
    requests_collection.insert_one({
        "bloodType": blood_type,
        "quantity": quantity,
        "status": "pending"
    })

    return jsonify({"status": "success", "message": "Emergency request submitted"}), 200

# Route to get pending requests (for admin)
@app.route('/api/pending-requests', methods=['GET'])
def get_pending_requests():
    pending_requests = list(requests_collection.find({}, {"_id": 0}))
    return jsonify(pending_requests), 200

# Route to get current inventory (for admin and hospitals)
@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    inventory_data = list(inventory_collection.find({}, {"_id": 0}))
    return jsonify(inventory_data), 200

# Route for submitting a hospital blood request
@app.route('/api/hospital-request', methods=['POST'])
def hospital_request():
    if session.get("role") != "hospital":
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.json
    blood_type = data.get("bloodType")
    quantity = data.get("quantity")

    if not blood_type or not quantity:
        return jsonify({"error": "Blood type and quantity are required"}), 400

    requests_collection.insert_one({
        "hospital": session.get("user"),
        "bloodType": blood_type,
        "quantity": quantity,
        "status": "pending"
    })

    return jsonify({"status": "success", "message": "Hospital request submitted"}), 200

# Route for hospitals to view available blood inventory
@app.route('/api/hospital-inventory', methods=['GET'])
def hospital_inventory():
    if session.get("role") != "hospital":
        return jsonify({"error": "Unauthorized access"}), 403

    inventory_data = list(inventory_collection.find({}, {"_id": 0}))
    return jsonify(inventory_data), 200

# Route for hospitals to view request status
@app.route('/api/hospital-request-status', methods=['GET'])
def hospital_request_status():
    if session.get("role") != "hospital":
        return jsonify({"error": "Unauthorized access"}), 403

    request_status = list(requests_collection.find({"hospital": session.get("user")}, {"_id": 0}))
    return jsonify(request_status), 200

# Route for hospitals to schedule a blood donation event
@app.route('/api/hospital-schedule-event', methods=['POST'])
def hospital_schedule_event():
    if session.get("role") != "hospital":
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.json
    event_name = data.get("eventName")
    event_date = data.get("eventDate")
    location = data.get("location")
    required_blood_types = data.get("requiredBloodTypes", [])

    if not event_name or not event_date or not location:
        return jsonify({"error": "Event name, date, and location are required"}), 400

    events_collection.insert_one({
        "hospital": session.get("user"),
        "eventName": event_name,
        "eventDate": event_date,
        "location": location,
        "requiredBloodTypes": required_blood_types
    })

    return jsonify({"status": "success", "message": "Event scheduled successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
