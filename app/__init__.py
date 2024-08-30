from flask import Flask
from config import config
from app.utils.db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db = init_db(app)

    return app

app = create_app()
