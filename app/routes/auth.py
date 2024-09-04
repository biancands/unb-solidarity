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
def update():
    data = request.get_json()
    email = data.get('email')
    new_email = data.get('new_email')
    new_password = data.get('new_password')
    new_first_name = data.get('new_first_name')
    new_last_name = data.get('new_last_name')

    user = User(mongo.db)
    existing_user = user.find_by_email(email)

    if not existing_user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    if new_email:
        existing_user['email'] = new_email
    if new_password:
        existing_user['password'] = new_password
    if new_first_name:
        existing_user['first_name'] = new_first_name
    if new_last_name:
        existing_user['last_name'] = new_last_name

    if user.update_user(existing_user):
        return jsonify({"message": "Dados da conta atualizados com sucesso"}), 200
    else:
        return jsonify({"message": "Erro ao atualizar dados da conta"}), 500

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
