from flask import Blueprint, request, jsonify
from app.utils.db import mongo
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User(mongo.db)
    if user.find_by_email(email):
        return jsonify({"message": "Usuário já existe"}), 409

    user_id = user.create_user(email, password)
    return jsonify({"message": "Usuário criado com sucesso", "user_id": user_id}), 201
