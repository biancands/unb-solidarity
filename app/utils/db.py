from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app: Flask):
    mongo.init_app(app)
    return mongo.db
