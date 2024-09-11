from flask import Flask
from config import config
from app.utils.db import init_db
from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.donations import donation_bp
from flask_qrcode import QRcode

qrcode = QRcode()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db = init_db(app)

    qrcode.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(donation_bp)

    return app

app = create_app()
