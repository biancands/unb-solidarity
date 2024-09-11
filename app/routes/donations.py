from io import BytesIO
from flask import Blueprint, Response, redirect, request, jsonify, render_template, session, url_for
import qrcode
from app.utils.db import mongo
from app.models import Donation
from flask_qrcode import QRcode
import requests
from bson.objectid import ObjectId

donation_bp = Blueprint('donation', __name__)

@donation_bp.route('/create_donation', methods=['GET'])
def create_donation_page():
    return render_template('donation_form.html')

@donation_bp.route('/create_donation', methods=['POST'])
def create_donation():
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('auth.login_page'))

    data = request.form
    item = data.get('item_description')
    destination = data.get('destination')

    address = get_address_from_gps(destination)

    user = mongo.db.users.find_one({"email": user_email})
    user_id = str(user['_id'])

    donation = Donation(mongo.db)
    donation_id = donation.create_donation(user_id, item, address)

    qr_code_url = url_for('donation.qr_code', donation_id=donation_id, _external=True)
    tracking_code = donation_id  # Ajuste aqui

    mongo.db.donations.update_one({"_id": ObjectId(donation_id)}, {"$set": {"tracking_code": tracking_code}})

    return render_template('donation_success.html', qr_code_url=qr_code_url, tracking_code=tracking_code)

def get_address_from_gps(destination):
    try:
        # Utilizando a API do OpenStreetMap (Nominatim) para buscar o endereço (restringido ao Brasil)
        api_url = f"https://nominatim.openstreetmap.org/search?q={destination}&countrycodes=BR&format=json"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if data:

                address = data[0]['display_name']
                return address
            else:
               
                return destination
        else:
            
            return destination
    except Exception as e:
        
        print(f"Erro ao obter endereço via GPS: {e}")
        return destination

@donation_bp.route('/qrcode/<donation_id>', methods=['GET'])
def qr_code(donation_id):
    # Cria uma instância do QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Adiciona dados ao QR Code
    qr.add_data(url_for('donation.qr_code', donation_id=donation_id, _external=True))
    qr.make(fit=True)
    
    # Gera a imagem do QR Code
    img = qr.make_image(fill='black', back_color='white')
    
    # Converte a imagem para bytes
    img_bytes = BytesIO()
    img.save(img_bytes)
    img_bytes.seek(0)
    
    # Retorna a imagem como uma resposta
    return Response(img_bytes, mimetype='image/png')
