from flask import Flask
from config import config
from app.utils.db import init_db
from app.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db = init_db(app)
    
    app.register_blueprint(auth_bp)

    return app

app = create_app()
