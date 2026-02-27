from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import json
import uuid
import os

departments_bp = Blueprint("departments", __name__)

DATA_FILE = os.path.join(os.getcwd(), "data", "departments.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@departments_bp.route("", methods=["GET"])
@jwt_required()
def get_departments():
    data = load_data()
    return jsonify({"count": len(data), "departments": data})

@departments_bp.route("", methods=["POST"])
@jwt_required()
def create_department():
    data = load_data()
    new_department = request.json
    new_department["id"] = str(uuid.uuid4())
    data.append(new_department)
    save_data(data)
    return jsonify(new_department), 201