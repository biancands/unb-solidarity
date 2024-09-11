"""
This module sets up the main routes for the Flask application.
"""

from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def index():
    """
    Render the index page.
    """
    return render_template('index.html')
