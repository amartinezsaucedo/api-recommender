from flask import Blueprint, request, jsonify, abort, make_response
from backend.recommender.controllers.recommendation import RecommendationController

recommendations = Blueprint('recommendations', __name__)

controller = RecommendationController()


@recommendations.get("/recommendations")
def recommend():
    query = request.args.get("query")
    algorithm = request.args.get("algorithm")
    model = request.args.get("model")
    try:
        return jsonify({"recommendations": controller.get_recommendations(query, algorithm, model)})
    except ValueError as e:
        abort(make_response(jsonify(message=str(e)), 404))

