#pylint: disable=line-too-long
"""
This module defines the routes for tracking donations in the application.
Routes:
    - /track_donations (GET): Track donations made by the logged-in user.
    - /register_donation_receipt (POST): Register the receipt of a donation and add media proof.
    - /statistics (GET): Display statistics about donations.
Functions:
    - track_donations(): Retrieves and displays donations along with their tracking and media information.
    - register_donation_receipt(): Registers a donation receipt event and adds media proof.
    - statistics(): Displays statistics about total donations, received donations, and donations by location.
"""

from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for
from app.utils.db import mongo
from app.models import Donation, Tracking, Media

tracking_bp = Blueprint('tracking', __name__)


@tracking_bp.route('/track_donations', methods=['GET'])
def track_donations():
    """
    Retrieves and displays donations along with their tracking and media information for the logged-in user.
    Redirects to the login page if the user is not logged in.
    """
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('auth.login_page'))

    user = mongo.db.users.find_one({"email": user_email})
    if not user:
        return redirect(url_for('auth.login_page'))

    donations = Donation(mongo.db).get_donations_by_user(user['_id'])
    donations_with_tracking = []

    tracking_model = Tracking(mongo.db)
    media_model = Media(mongo.db)

    for donation in donations:
        tracking_info = tracking_model.get_tracking_info(donation['_id'])
        media_info = media_model.get_media_by_donation(donation['_id'])
        donations_with_tracking.append({
            "donation": donation,
            "tracking": tracking_info,
            "media": media_info
        })

    return render_template('track_donations.html',
                           donations=donations_with_tracking)


@tracking_bp.route('/register_donation_receipt', methods=['POST'])
def register_donation_receipt():
    """
    Registers a donation receipt event and adds media proof.
    """
    data = request.form
    donation_id = data.get('donation_id')
    media_url = data.get('media_url')

    tracking_model = Tracking(mongo.db)
    media_model = Media(mongo.db)

    tracking_model.add_tracking_event(donation_id,
                                      location="Recebido",
                                      status="Recebido")

    media_model.add_media(donation_id, media_url)

    return jsonify({"message":
                    "Doação recebida e comprovada com sucesso"}), 200


@tracking_bp.route('/statistics', methods=['GET'])
def statistics():
    """
    Displays statistics about total donations, received donations, and donations by location.
    """
    total_donations = mongo.db.donations.count_documents({})
    total_received = mongo.db.tracking.count_documents({"status": "Recebido"})
    donations_by_location = mongo.db.donations.aggregate([{
        "$group": {
            "_id": "$destination",
            "count": {
                "$sum": 1
            }
        }
    }])

    return render_template('statistics.html',
                           total_donations=total_donations,
                           total_received=total_received,
                           donations_by_location=donations_by_location)
