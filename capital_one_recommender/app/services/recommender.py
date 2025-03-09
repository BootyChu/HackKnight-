import requests
import pandas as pd
from app.utils.models import QuestionnaireResponse
from flask import jsonify

# Nessie API Configuration
NESSIE_API_KEY = "bb677a58f38e2f66d5f548a2a923366e"
NESSIE_BASE_URL = "http://api.nessieisreal.com"

def get_latest_user_response():
    """Fetch the latest questionnaire response from the database."""
    return QuestionnaireResponse.query.order_by(QuestionnaireResponse.id.desc()).first()

def get_mock_customers():
    """Fetch mock customer profiles from Nessie API."""
    response = requests.get(f"{NESSIE_BASE_URL}/customers?key={NESSIE_API_KEY}")
    if response.status_code == 200:
        return response.json()
    return []

def match_user_to_mock_profile(user_income, user_credit_score):
    """Find a similar user from Nessie’s mock data."""
    customers = get_mock_customers()
    
    best_match = None
    min_diff = float("inf")

    for customer in customers:
        customer_income = customer.get("income", 50000)  # Default to 50K
        customer_credit = customer.get("credit_score", 650)  # Default to 650

        diff = abs(customer_income - user_income) + abs(customer_credit - user_credit_score)
        if diff < min_diff:
            min_diff = diff
            best_match = customer

    return best_match

def load_card_data():
    """Load credit card data from CSV and clean column names."""
    df = pd.read_csv("app/static/data/cards.csv")
    df.columns = df.columns.str.strip()  # Remove trailing spaces
    return df

def recommend_card():
    """Generate a credit card recommendation based on user input."""
    
    # Step 1: Get the latest user input from the database
    user = get_latest_user_response()
    if not user:
        return []  # Return an empty list instead of a dictionary with an error message

    # Step 2: Match user with a similar Nessie mock customer
    mock_customer = match_user_to_mock_profile(user.annual_income, user.credit_score)

    # Step 3: Load available credit cards
    df = load_card_data()
    
    # Step 4: Apply filtering based on user spending categories
    spending_categories = [
        ("travel", user.travel),
        ("dining", user.dining),
        ("groceries", user.groceries),
        ("gas_automotive", user.gas_automotive),
        ("shopping", user.shopping),
        ("entertainment", user.entertainment),
        ("bills_utilities", user.bills_utilities),
    ]
    selected_categories = [cat[0] for cat in spending_categories if cat[1]]

    df["match_score"] = df["Card Type"].apply(lambda x: sum(cat in x.lower() for cat in selected_categories))

    # Step 5: Filter based on financial status
    if user.annual_income < 50000:
        df = df[df["Annual Fee"] == "$0"]

    df = df[df["Credit Level"].apply(lambda x: check_credit_eligibility(user.credit_score, x))]

    # Step 6: Apply user preferences
    if user.no_foreign_fees:
        df = df[df["Transfer Info"].str.contains("No foreign transaction fees", na=False)]

    if user.prefer_cashback:
        df = df[df["Card Type"] == "Cashback"]

    # Step 7: Adjust based on mock user spending trends (if available)
    if mock_customer:
        df["adjusted_score"] = df["match_score"] + 1  # Simple score boost for similarity
    else:
        df["adjusted_score"] = df["match_score"]

    # Step 8: Get the top recommendations
    if df.empty:
        return []  # Return an empty list instead of a message dictionary

    # Select the top 3 recommendations
    top_recommendations = df.sort_values(by="adjusted_score", ascending=False).head(3)

    # Convert to a list of dictionaries
    recommended_cards = top_recommendations.to_dict(orient="records")

    return recommended_cards  # Ensure it's a LIST of DICTIONARIES


def check_credit_eligibility(user_score, card_requirement):
    """Checks if the user's credit score meets the card's requirement."""
    score_map = {"Poor": 300, "Fair": 580, "Good": 670, "Very Good": 740, "Excellent": 800}
    required_score = score_map.get(card_requirement.split("-")[0], 300)
    return user_score >= required_score