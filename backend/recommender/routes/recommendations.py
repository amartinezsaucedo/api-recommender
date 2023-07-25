from flask import Blueprint, request, jsonify
from backend.recommender.controllers.recommendation import RecommendationController

recommendations = Blueprint('recommendations', __name__)

controller = RecommendationController()


@recommendations.get("/recommendations")
def recommend():
    query = request.args.get("query")
    algorithm = request.args.get("algorithm")
    model = request.args.get("model")
    return jsonify({"recommendations": controller.get_recommendations(query, algorithm, model)})
