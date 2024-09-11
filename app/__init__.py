
"""
This module initializes the Flask application and registers the necessary blueprints and extensions.
Modules:
    Flask: The Flask application instance.
    config: Configuration settings for the application.
    init_db: Function to initialize the database.
    auth_bp: Blueprint for authentication routes.
    main_bp: Blueprint for main application routes.
    donation_bp: Blueprint for donation-related routes.
    tracking_bp: Blueprint for tracking-related routes.
    statistics_bp: Blueprint for statistics-related routes.
    QRcode: Extension for generating QR codes.
Functions:
    create_app(): Creates and configures the Flask application instance.
"""

from flask import Flask
from flask_qrcode import QRcode
from config import config
from app.utils.db import init_db
from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.donations import donation_bp
from app.routes.tracking import tracking_bp
from app.routes.statistics import statistics_bp

qrcode = QRcode()


def create_app():

    """
    Creates and configures the Flask application instance.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__) #pylint: disable=redefined-outer-name
    app.config.from_object(config)

    db = init_db(app) #pylint: disable=unused-variable
    qrcode.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(donation_bp)
    app.register_blueprint(tracking_bp)
    app.register_blueprint(statistics_bp)

    return app


app = create_app()
