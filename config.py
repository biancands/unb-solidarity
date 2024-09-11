"""
Configuration module for UNB Solidarity application.
"""

import os


class Config:
    """
    Configuration class for UNB Solidarity application.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    MONGO_URI = os.environ.get(
        'MONGO_URI') or 'mongodb://localhost:27017/unb_solidarity'


config = Config()
