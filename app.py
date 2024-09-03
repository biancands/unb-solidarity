from flask import Flask, render_template, request, redirect, url_for, session, flash
import qrcode
from io import BytesIO
import os

# Inicialize o app Flask
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Altere 'sua_chave_secreta_aqui' para uma chave secreta real

# Simulação de um "banco de dados" para usuários e doações (em memória)
users = {}
donations = []

# Página Inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página de Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        cpf = request.form['cpf']
        birth_date = request.form['birth_date']

        # Validação simples
        if email in users:
            flash('E-mail já registrado. Por favor, faça login.')
            return redirect(url_for('login'))

        # Salvar o usuário no "banco de dados"
        users[email] = {
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
            'cpf': cpf,
            'birth_date': birth_date
        }

        flash('Registro bem-sucedido! Por favor, faça login.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Página de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.get(email)
        if user and user['password'] == password:
            # Usuário autenticado com sucesso
            session['user'] = user
            flash('Login bem-sucedido!')
            return redirect(url_for('profile'))
        else:
            flash('Credenciais inválidas. Por favor, tente novamente.')

    return render_template('index.html')

# Página de Perfil
@app.route('/profile')
def profile():
    if 'user' not in session:
        flash('Por favor, faça login para acessar o perfil.')
        return redirect(url_for('login'))
    
    # Obtém o usuário da sessão
    user = session['user']
    return render_template('profile.html', user=user)

# Página de Doação
@app.route('/donation', methods=['GET', 'POST'])
def donation():
    if 'user' not in session:
        flash('Por favor, faça login para fazer uma doação.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        item = request.form['item']
        destination = request.form['destination']
        
        # Gerar QRCode
        qr = qrcode.make(f"Item: {item}, Destino: {destination}")
        buf = BytesIO()
        qr.save(buf, format='PNG')
        buf.seek(0)
        
        qr_filename = f"static/qrcodes/{item}_qrcode.png"
        os.makedirs(os.path.dirname(qr_filename), exist_ok=True)
        with open(qr_filename, 'wb') as f:
            f.write(buf.getvalue())
        
        donations.append({'item': item, 'destination': destination, 'qrcode': qr_filename})
        flash('Doação registrada com sucesso!')

        return redirect(url_for('profile'))

    return render_template('donation.html')

# Página de Visualização de Doações
@app.route('/view_donations')
def view_donations():
    if 'user' not in session:
        flash('Por favor, faça login para visualizar as doações.')
        return redirect(url_for('login'))

    return render_template('view_donations.html', donations=donations)

# Rota de Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Você saiu com sucesso.')
    return redirect(url_for('index'))

# Rota de Exclusão de Conta
@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user' not in session:
        flash('Por favor, faça login para excluir sua conta.')
        return redirect(url_for('login'))

    # Remove o usuário do "banco de dados"
    user = session.pop('user')  # Remove o usuário da sessão
    email = user.get('email')  # Obtém o e-mail do usuário
    if email in users:
        del users[email]  # Remove o usuário do dicionário de usuários
        flash('Conta excluída com sucesso.')
    else:
        flash('Conta não encontrada.')

    return redirect(url_for('index'))

# Iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)
