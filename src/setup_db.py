from app.database import db
from app.redis import cache
from app.user import User

from dotenv import load_dotenv
load_dotenv(dotenv_path="app/.env")
import os

if __name__ == "__main__":
    input("This will initialize the database. Press Enter to continue...")
    db.initialize_database()
    cache.flush()
    print("Database Initialized")
    print("Creating admin user......")
    admin = User(
        email=os.getenv("SUDO_ADMIN_EMAIL"),
        password=os.getenv("SUDO_ADMIN_PASSWORD"),
        name= "Admin",
        is_admin= True,
        phone_number="1234567890"
    )
    admin.create()
    print("Admin created Successfully")