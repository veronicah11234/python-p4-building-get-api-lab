# Import necessary modules and models
# from server import db
from app import create_app, db
from model import Bakery, BakedGood
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define a function to seed the database with initial data
def seed_data():
    app = create_app()
    with app.app_context():
        # Your data seeding logic here
        bakeries = [
            Bakery(name='Bakery 1'),
            Bakery(name='Bakery 2'),
            # Add more bakery instances as needed
        ]
        db.session.add_all(bakeries)
        db.session.commit()

# Call the seed function to populate the database
if __name__ == "__main__":
    seed_data()
