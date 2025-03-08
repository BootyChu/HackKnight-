from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def init_db(app):
    """Initialize the database"""
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()