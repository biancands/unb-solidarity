"""
This module contains the models for the unb-solidarity application.

Classes:
    User: Manages user-related operations.
    Donation: Manages donation-related operations.
    Tracking: Manages tracking-related operations.
    Media: Manages media-related operations.
"""

import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId


#pylint: disable=missing-class-docstring, missing-function-docstring
class User:

    def __init__(self, db):
        self.db = db

    def create_user(self, email, password, first_name, last_name):
        hashed_password = generate_password_hash(password)
        user_id = self.db.users.insert_one({
            "email": email,
            "password": hashed_password,
            "first_name": first_name,
            "last_name": last_name
        }).inserted_id
        return str(user_id)

    def find_by_email(self, email):
        return self.db.users.find_one({"email": email})

    def verify_password(self, stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)

    def update_user(self, email, new_data):
        result = self.db.users.update_one({"email": email}, {"$set": new_data})
        return result.modified_count > 0

    def delete_user(self, email):
        result = self.db.users.delete_one({"email": email})
        return result.deleted_count > 0


class Donation:

    def __init__(self, db):
        self.db = db

    def create_donation(self, user_id, item, destination):
        donation_id = self.db.donations.insert_one({
            "user_id":
            ObjectId(user_id),
            "item":
            item,
            "destination":
            destination,
            "tracking_code":
            None,
            "created_at":
            datetime.datetime.utcnow()
        }).inserted_id
        return str(donation_id)

    def get_donations_by_user(self, user_id):
        return list(self.db.donations.find({"user_id": ObjectId(user_id)}))


class Tracking:

    def __init__(self, db):
        self.db = db

    def add_tracking_event(self, donation_id, location, status):
        event_id = self.db.tracking.insert_one({
            "donation_id":
            ObjectId(donation_id),
            "location":
            location,
            "status":
            status,
            "timestamp":
            datetime.datetime.utcnow()
        }).inserted_id
        return str(event_id)

    def get_tracking_info(self, donation_id):
        return list(
            self.db.tracking.find({"donation_id": ObjectId(donation_id)}))


class Media:

    def __init__(self, db):
        self.db = db

    def add_media(self, donation_id, url):
        media_id = self.db.media.insert_one({
            "donation_id":
            ObjectId(donation_id),
            "url":
            url
        }).inserted_id
        return str(media_id)

    def get_media_by_donation(self, donation_id):
        return list(self.db.media.find({"donation_id": ObjectId(donation_id)}))
