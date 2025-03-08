from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from app.utils.database import db


bcrypt = Bcrypt()

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Hashed password
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Top Spending Categories (Boolean Flags)
    travel = db.Column(db.Boolean, default=False)
    dining = db.Column(db.Boolean, default=False)
    groceries = db.Column(db.Boolean, default=False)
    gas_automotive = db.Column(db.Boolean, default=False)
    shopping = db.Column(db.Boolean, default=False)
    entertainment = db.Column(db.Boolean, default=False)
    bills_utilities = db.Column(db.Boolean, default=False)
    
    # Financial Information
    annual_income = db.Column(db.Integer, nullable=False, default=0)  # Stores Approximate Annual Income
    credit_score = db.Column(db.Integer, nullable=False, default=0)  # Stores Estimated Credit Score

    # User Preferences (Boolean Flags)
    pay_balance_in_full = db.Column(db.Boolean, default=False)
    no_foreign_fees = db.Column(db.Boolean, default=False)
    prefer_cashback = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """Hash password before storing"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check hashed password"""
        return bcrypt.check_password_hash(self.password, password)