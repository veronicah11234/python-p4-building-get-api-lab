from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from server.route import main_bp

# Initialize db outside of the create_app function
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    # Initialize db with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints using absolute import
    app.register_blueprint(main_bp)

    return app
