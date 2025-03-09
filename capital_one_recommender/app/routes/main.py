import os
from flask import Blueprint, render_template, request, render_template, redirect, url_for, flash, jsonify
from app.services.recommender import recommend_card
from app.utils.models import db, QuestionnaireResponse
from app.utils.database import init_db
from app.routes.auth import auth
from groq import Groq
import datetime
from dotenv import load_dotenv
import json
import re

# ✅ Create the Blueprint
main = Blueprint('main', __name__)

load_dotenv()
# Initialize Groq API Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ✅ Define Routes
@main.route('/')
def home():
    return render_template('index.html')


@main.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')

@main.route('/results')
def results():
    recommendations = recommend_card()  # Ensure this returns a LIST of DICTIONARIES
    if not isinstance(recommendations, list):  # Fix case where a single string is returned
        recommendations = []
    return render_template('results.html', recommendations=recommendations)


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
    return render_template('congrats.html')  

@main.route('/about')
def about():
    return render_template('about_us.html')


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
        # Extract boolean values correctly
        pay_balance_in_full = request.form.get('pay_balance_in_full') is not None
        no_foreign_fees = request.form.get('no_foreign_fees') is not None
        prefer_cashback = request.form.get('prefer_cashback') is not None

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


@main.route("/help_support", methods=["GET", "POST"])
def help_support():
    if request.method == "POST":
        # Fetch the latest user questionnaire response
        user_data = QuestionnaireResponse.query.order_by(QuestionnaireResponse.date_created.desc()).first()
        
        if not user_data:
            return jsonify({"error": "No user data found"}), 400

        # Format user preferences for AI prompt
        user_info = f"""
        Travel: {user_data.travel}, Dining: {user_data.dining}, Groceries: {user_data.groceries},
        Gas & Automotive: {user_data.gas_automotive}, Shopping: {user_data.shopping},
        Entertainment: {user_data.entertainment}, Bills & Utilities: {user_data.bills_utilities},
        Annual Income: {user_data.annual_income}, Credit Score: {user_data.credit_score},
        Pay Balance in Full: {user_data.pay_balance_in_full}, No Foreign Fees: {user_data.no_foreign_fees},
        Prefer Cashback: {user_data.prefer_cashback}
        """

        # AI Chatbot Query (Forcing JSON Output)
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": f"Help me determine the top 3 capital one credit cards based on this user profile: {user_info}. "
                               f"ONLY return a valid JSON array with exactly 3 items using this format:\n"
                               f'[{{"card_name": "string", "credit_level": "string", "reward": "string", '
                               f'"annual_fee": "string", "purchase_rate": "string", "transfer_info": "string"}}]. '
                               f"ONLY return a JSON array with exactly 3 items. DO NOT include any text before or after the JSON array."
                               #f"Do not return the title of the card with 'Capital One' in the header, you can still say cash rewards credit card etc"
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        # **Debugging: Print AI Raw Response**
        raw_response = completion.choices[0].message.content
        print("🔹 Raw AI Response:", raw_response)

        # **Extract JSON Block from AI Response**
        match = re.search(r"\[.*\]", raw_response, re.DOTALL)  # Extract anything between square brackets
        if not match:
            print("❌ No JSON Array Found in AI Response!")
            return jsonify({"error": "AI response did not contain valid JSON"}), 500

        json_string = match.group(0)  # Get the matched JSON array

        # **Try to Parse JSON Response**
        try:
            recommended_cards = json.loads(json_string)
        except json.JSONDecodeError:
            print("❌ JSON Decoding Error: AI Response is not valid JSON!")
            return jsonify({"error": "AI response could not be processed"}), 500

        print("✅ Parsed Cards:", recommended_cards)

        return jsonify({"cards": recommended_cards})

    return render_template("help_support.html")