from flask import Blueprint, request, jsonify, render_template
from app.utils.db import mongo
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    user = User(mongo.db)
    if user.find_by_email(email):
        return jsonify({"message": "Usuário já existe"}), 409

    user_id = user.create_user(email, password, first_name, last_name)
    return jsonify({"message": "Usuário criado com sucesso", "user_id": user_id}), 201

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User(mongo.db)
    existing_user = user.find_by_email(email)

    if not existing_user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    existing_password = user.verify_password(existing_user['password'], password)

    if existing_password:
        return jsonify({"message": "Login bem-sucedido"}), 200
    else:
        return jsonify({"message": "Senha incorreta"}), 401

@auth_bp.route('/update_user', methods=['PUT'])
def update_user():
    data = request.get_json()
    email = data.get('email')
    update_data = data.get('update_data')

    user = User(mongo.db)
    if not user.find_by_email(email):
        return jsonify({"message": "Usuário não encontrado"}), 404

    if user.update_user(email, update_data):
        return jsonify({"message": "Usuário atualizado com sucesso"}), 200
    else:
        return jsonify({"message": "Erro ao atualizar usuário"}), 500

@auth_bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    email = data.get('email')

    user = User(mongo.db)
    if not user.find_by_email(email):
        return jsonify({"message": "Usuário não encontrado"}), 404

    if user.delete_user(email):
        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    else:
        return jsonify({"message": "Erro ao excluir usuário"}), 500
