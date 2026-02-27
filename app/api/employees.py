from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import json
import uuid

employees_bp = Blueprint("employees", __name__)

DATA_FILE = "data/employees.json"

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@employees_bp.route("", methods=["GET"])
@jwt_required()
def get_employees():
    data = load_data()
    return jsonify({"count": len(data), "employees": data})

@employees_bp.route("", methods=["POST"])
@jwt_required()
def create_employee():
    data = load_data()
    new_employee = request.json
    new_employee["id"] = str(uuid.uuid4())
    data.append(new_employee)
    save_data(data)
    return jsonify(new_employee), 201