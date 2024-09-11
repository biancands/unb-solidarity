"""
This module defines the routes for handling donations in the application.
Routes:
    - /create_donation (GET): Renders the donation creation form.
    - /create_donation (POST): Handles the creation of a new donation.
    - /qrcode/<donation_id> (GET): Generates and returns a QR code for the donation.
    - /register_donation (GET): Renders the donation registration form.
    - /register_donation (POST): Handles the registration of a donation with media.
Functions:
    - create_donation_page(): Renders the donation creation form.
    - create_donation(): Handles the creation of a new donation.
    - get_address_from_gps(destination): Retrieves the address from GPS coordinates.
    - qr_code(donation_id): Generates and returns a QR code for the donation.
    - register_donation_page(): Renders the donation registration form.
    - register_donation(): Handles the registration of a donation with media.
"""
from io import BytesIO
import os
from flask import Blueprint, Response, flash, redirect, request, jsonify
from flask import render_template, session, url_for
import qrcode
from werkzeug.utils import secure_filename
import requests
from bson.objectid import ObjectId
from app.utils.db import mongo
from app.models import Donation, Tracking, Media

donation_bp = Blueprint('donation', __name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@donation_bp.route('/create_donation', methods=['GET'])
def create_donation_page():
    """
    Renders the donation creation form.
    """
    return render_template('donation_form.html')


@donation_bp.route('/create_donation', methods=['POST'])
def create_donation():
    """
    Handles the creation of a new donation.
    """
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

    qr_code_url = url_for('donation.qr_code',
                          donation_id=donation_id,
                          _external=True)
    tracking_code = donation_id

    mongo.db.donations.update_one({"_id": ObjectId(donation_id)},
                                  {"$set": {
                                      "tracking_code": tracking_code
                                  }})

    return render_template('donation_success.html',
                           qr_code_url=qr_code_url,
                           tracking_code=tracking_code)


#pylint: disable=line-too-long
def get_address_from_gps(destination):
    """
    Retrieves the address from GPS coordinates using the Nominatim API.
    
    Args:
        destination (str): The GPS coordinates or location query.
    
    Returns:
        str: The address corresponding to the GPS coordinates or the original destination if not found.
    """
    try:
        api_url = f"https://nominatim.openstreetmap.org/search?q={destination}&countrycodes=BR&format=json"
        response = requests.get(api_url)  # pylint: disable=missing-timeout

        if response.status_code == 200:
            data = response.json()
            if data:
                address = data[0]['display_name']
                return address
            else:
                return destination
        else:
            return destination
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Erro ao obter endereço via GPS: {e}")
        return destination


@donation_bp.route('/qrcode/<donation_id>', methods=['GET'])
def qr_code(donation_id):
    """
    Generates and returns a QR code for the donation.
    
    Args:
        donation_id (str): The ID of the donation.
    
    Returns:
        Response: A Flask response object containing the QR code image.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(
        url_for('donation.qr_code', donation_id=donation_id, _external=True))
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    img_bytes = BytesIO()
    img.save(img_bytes)
    img_bytes.seek(0)

    return Response(img_bytes, mimetype='image/png')


@donation_bp.route('/register_donation', methods=['GET'])
def register_donation_page():
    """
    Renders the donation registration form.
    """
    return render_template('register_donation.html')


@donation_bp.route('/register_donation', methods=['POST'])
def register_donation():
    """
    Handles the registration of a donation with media.
    """
    donation_id = request.form.get('donation_id')
    media_file = request.files.get('media')

    if not donation_id or not media_file:
        return jsonify(
            {"message": "Código de doação ou comprovante não fornecido"}), 400

    donation = mongo.db.donations.find_one({"_id": ObjectId(donation_id)})
    if not donation:
        return jsonify({"message": "Doação não encontrada"}), 404

    filename = secure_filename(media_file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    media_file.save(file_path)

    tracking_model = Tracking(mongo.db)
    tracking_model.add_tracking_event(donation_id, "Local Recebido",
                                      "Recebido")

    media_model = Media(mongo.db)

    media_model.add_media(donation_id, filename)

    flash('Doação registrada com sucesso!', 'success')
    return redirect(url_for('auth.profile_page'))
