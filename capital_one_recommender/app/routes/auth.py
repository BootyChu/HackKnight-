from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.utils.models import db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)  # Define 'auth' Blueprint

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        print(f"Attempting to register: {username}, {email}")  # ✅ Debugging print

        # Check if email or username already exists
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            print("❌ Registration failed: Username or Email already exists!")  # ✅ Debugging print
            flash("Username or Email already exists!", "danger")
            return redirect(url_for('auth.register'))

        # Spending categories (Checkbox values are 'on' if checked)
        travel = 'travel' in request.form
        dining = 'dining' in request.form
        groceries = 'groceries' in request.form
        gas_automotive = 'gas_automotive' in request.form
        shopping = 'shopping' in request.form
        entertainment = 'entertainment' in request.form
        bills_utilities = 'bills_utilities' in request.form

        # Financial Information (Convert input to integers)
        try:
            annual_income = int(request.form['annual_income'])
            credit_score = int(request.form['credit_score'])
        except ValueError:
            print("❌ Error: Invalid number format for income or credit score")  # ✅ Debugging print
            flash("Please enter valid numbers for income and credit score.", "danger")
            return redirect(url_for('auth.register'))

        # User Preferences (Checkbox values are 'on' if checked)
        pay_balance_in_full = 'pay_balance_in_full' in request.form
        no_foreign_fees = 'no_foreign_fees' in request.form
        prefer_cashback = 'prefer_cashback' in request.form

        # Create new user
        new_user = User(
            username=username,
            email=email,
            travel=travel,
            dining=dining,
            groceries=groceries,
            gas_automotive=gas_automotive,
            shopping=shopping,
            entertainment=entertainment,
            bills_utilities=bills_utilities,
            annual_income=annual_income,
            credit_score=credit_score,
            pay_balance_in_full=pay_balance_in_full,
            no_foreign_fees=no_foreign_fees,
            prefer_cashback=prefer_cashback
        )
        new_user.set_password(password)  # Hash password

        # Save to database
        try:
            db.session.add(new_user)
            db.session.commit()
            print(f"✅ User added: {new_user.username}, {new_user.email}")  # ✅ Debugging print
            flash("Account created successfully! You can now log in.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"❌ Error saving user: {str(e)}")  # ✅ Debugging print
            db.session.rollback()  # Rollback changes in case of failure
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form['user_input']  # Can be username or email
        password = request.form['password']

        # Check if the user exists (search by email OR username)
        user = User.query.filter((User.email == user_input) | (User.username == user_input)).first()

        if user and user.check_password(password):
            flash("Logged in successfully!", "success")
            return redirect(url_for('main.dashboard'))  # Redirect to dashboard

        flash("Invalid username/email or password!", "danger")

    return render_template('login.html')

@auth.route('/debug/users')
def debug_users():
    users = User.query.all()
    return {"users": [{"id": u.id, "username": u.username, "email": u.email} for u in users]}