from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import json
import uuid
import os

salaries_bp = Blueprint("salaries", __name__)

DATA_FILE = os.path.join(os.getcwd(), "data", "salaries.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@salaries_bp.route("", methods=["GET"])
@jwt_required()
def get_salaries():
    data = load_data()
    return jsonify({"count": len(data), "salaries": data})

@salaries_bp.route("", methods=["POST"])
@jwt_required()
def create_salary():
    data = load_data()
    new_salary = request.json
    new_salary["id"] = str(uuid.uuid4())
    data.append(new_salary)
    save_data(data)
    return jsonify(new_salary), 201