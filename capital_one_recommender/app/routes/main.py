# from flask import Flask, render_template, Blueprint
# from app.utils.models import db
# from app.utils.database import init_db
# from app.routes.auth import auth

# app = Flask(__name__, static_folder="../static", template_folder="../templates")

# init_db(app) 

# # Register Blueprints
# app.register_blueprint(auth, url_prefix="/")  # Register 'auth' Blueprint


# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/questionnaire')
# def questionnaire():
#     return render_template('questionnaire.html')

# @app.route('/results')
# def results():
#     return render_template('results.html')

# @app.route('/comparison')
# def comparison():
#     return render_template('comparison.html')

# @app.route('/education')
# def education():
#     return render_template('education.html')

# @app.route('/accessibility')
# def accessibility():
#     return render_template('accessibility.html')

# @app.route('/features')
# def features():
#     return render_template('features.html')

# @app.route('/feedback')
# def feedback():
#     return render_template('feedback.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Blueprint, render_template, request, render_template, redirect, url_for, flash, jsonify
from app.utils.models import db, QuestionnaireResponse
from app.utils.database import init_db
from app.routes.auth import auth

# ✅ Create the Blueprint
main = Blueprint('main', __name__)

# ✅ Define Routes
@main.route('/')
def home():
    return render_template('index.html')


@main.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')

@main.route('/results')
def results():
    return render_template('results.html')

@main.route('/comparison')
def comparison():
    return render_template('comparison.html')

@main.route('/education')
def education():
    return render_template('education.html')

@main.route('/accessibility')
def accessibility():
    return render_template('accessibility.html')

@main.route('/features')
def features():
    return render_template('features.html')

@main.route('/feedback')
def feedback():
    return render_template('feedback.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/congrats')
def congrats():
    return render_template('congrats.html')  # Ensure this template exists

@main.route('/submit_questionnaire', methods=['POST'])
def submit_questionnaire():
    try:
        # Extract boolean fields (checkboxes)
        travel = 'travel' in request.form
        dining = 'dining' in request.form
        groceries = 'groceries' in request.form
        gas_automotive = 'gas_automotive' in request.form
        shopping = 'shopping' in request.form
        entertainment = 'entertainment' in request.form
        bills_utilities = 'bills_utilities' in request.form

        # Extract numerical fields with default values
        annual_income = request.form.get('annual_income', '0').strip()
        credit_score = request.form.get('credit_score', '0').strip()

        # Convert to integers safely
        try:
            annual_income = int(annual_income)
        except ValueError:
            flash("Invalid input for Annual Income. Please enter a number.", "danger")
            return redirect(url_for('main.questionnaire'))

        try:
            credit_score = int(credit_score)
        except ValueError:
            flash("Invalid input for Credit Score. Please enter a number.", "danger")
            return redirect(url_for('main.questionnaire'))

        # Extract user preferences
        pay_balance_in_full = 'pay_balance_in_full' in request.form
        no_foreign_fees = 'no_foreign_fees' in request.form
        prefer_cashback = 'prefer_cashback' in request.form

        # ✅ Debugging: Print values to confirm they are captured correctly
        print(f"Travel: {travel}, Dining: {dining}, Groceries: {groceries}")
        print(f"Annual Income: {annual_income}, Credit Score: {credit_score}")
        print(f"Preferences - Pay Balance in Full: {pay_balance_in_full}, No Foreign Fees: {no_foreign_fees}, Prefer Cashback: {prefer_cashback}")

        # ✅ Save to database (assuming you have a model for questionnaire responses)
        new_response = QuestionnaireResponse(
            travel=travel, dining=dining, groceries=groceries, gas_automotive=gas_automotive,
            shopping=shopping, entertainment=entertainment, bills_utilities=bills_utilities,
            annual_income=annual_income, credit_score=credit_score,
            pay_balance_in_full=pay_balance_in_full, no_foreign_fees=no_foreign_fees, prefer_cashback=prefer_cashback
        )

        db.session.add(new_response)
        db.session.commit()

        flash("Form submitted successfully!", "success")
        return redirect(url_for('main.results'))

    except Exception as e:
        print(f"❌ Error processing form: {e}")  # ✅ Debugging print
        flash("An error occurred while submitting the form. Please try again.", "danger")
        return redirect(url_for('main.questionnaire'))

@main.route('/debug/questionnaire_responses', methods=['GET'])
def debug_questionnaire_responses():
    responses = QuestionnaireResponse.query.all()

    # Format as JSON for easier debugging
    response_list = [
        {
            "id": response.id,
            "travel": response.travel,
            "dining": response.dining,
            "groceries": response.groceries,
            "gas_automotive": response.gas_automotive,
            "shopping": response.shopping,
            "entertainment": response.entertainment,
            "bills_utilities": response.bills_utilities,
            "annual_income": response.annual_income,
            "credit_score": response.credit_score,
            "pay_balance_in_full": response.pay_balance_in_full,
            "no_foreign_fees": response.no_foreign_fees,
            "prefer_cashback": response.prefer_cashback,
        }
        for response in responses
    ]

    return jsonify(response_list)  # Returns all stored questionnaire responses as JSON