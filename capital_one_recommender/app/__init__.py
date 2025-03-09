import os
from flask import Flask
from flask_migrate import Migrate
from app.utils.models import db
from app.routes.auth import auth
from app.routes.main import main
from app.routes.api import api  # ✅ Import the API blueprint

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ✅ Load SECRET_KEY from environment variables for security
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "super_secret_key")

    # ✅ Database Configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ Initialize database and migrations
    db.init_app(app)
    Migrate(app, db)  # 🔹 Adds Flask-Migrate support

    # ✅ Register Blueprints
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(api, url_prefix="/")  # ✅ Register API Blueprint

    return app