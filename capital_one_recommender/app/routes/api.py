from flask import Blueprint, jsonify
from app.services.recommender import recommend_card

api = Blueprint('api', __name__)

@api.route('/recommend', methods=['GET'])
def get_recommendation():
    recommendation = recommend_card()
    return jsonify(recommendation)