from .auth import get_password_hash
from .database import MongoConnection



admin_user = {
    "username": "admin",
    "hashed_password": get_password_hash("adminpassword"),
    "is_admin": True
}

with MongoConnection() as mongo:
    mongo.user_collection.insert_one(admin_user)

