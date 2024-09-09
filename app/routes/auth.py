from flask import Blueprint, redirect, request, jsonify, render_template, session, url_for
from app.utils.db import mongo
from app.models import User

auth_bp = Blueprint('auth', __name__)

#EU001
@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

#EU001
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

#EU002
@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('index.html')

#EU002
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
        session['user_email'] = email
        return jsonify({"message": "Login bem-sucedido"}), 200
    else:
        return jsonify({"message": "Senha incorreta"}), 401

#EU006
#EU007
@auth_bp.route('/profile', methods=['GET'])
def profile_page():

    user_email = session.get('user_email')
    
    if not user_email:
        return redirect(url_for('auth.login_page'))
    
    user = User(mongo.db).find_by_email(user_email)
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    return render_template('profile.html', user=user)

#EU003
@auth_bp.route('/update_user_page', methods=['GET'])
def update_user_page():
    return render_template('update_user.html')


#EU003
@auth_bp.route('/update_user', methods=['PUT'])
def update_user():
    data = request.get_json()
    email = data.get('email')

    if not email:
        email = session.get('user_email')
        if not email:
            return jsonify({"message": "Usuário não logado"}), 403

    user = User(mongo.db)
    existing_user = user.find_by_email(email)

    if not existing_user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    new_data = {}
    if data.get('new_email'):
        new_data['email'] = data.get('new_email')
    if data.get('new_password'):
        new_data['password'] = data.get('new_password')
    if data.get('new_first_name'):
        new_data['first_name'] = data.get('new_first_name')
    if data.get('new_last_name'):
        new_data['last_name'] = data.get('new_last_name')

    if not new_data:
        return jsonify({"message": "Nenhuma informação fornecida para atualização"}), 400

    if user.update_user(email, new_data):
        return jsonify({"message": "Dados da conta atualizados com sucesso"}), 200
    else:
        return jsonify({"message": "Erro ao atualizar dados da conta"}), 500


#EU004    
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
    
#EU005
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_email', None)
    return redirect(url_for('auth.login_page')) 

