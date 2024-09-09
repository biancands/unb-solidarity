from flask import Blueprint, redirect, request, jsonify, render_template, session, url_for
from app.utils.db import mongo
from app.models import User

donation_bp = Blueprint('donation', __name__)

@donation_bp.route('/create_donation', methods=['GET'])
def create_donation():
    return render_template('donation_form.html')