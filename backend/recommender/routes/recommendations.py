from flask import Blueprint, request, jsonify, abort, make_response
from backend.recommender.controllers.recommendation import RecommendationController

recommendations = Blueprint('recommendations', __name__)

controller = RecommendationController.instance()


@recommendations.get("/recommendations")
def recommend():
    try:
        query = request.args.get("query")
        algorithm = request.args.get("algorithm")
        model = request.args.get("model")
        k = int(request.args.get("k"))
        return jsonify(controller.get_recommendations(query, algorithm, model, k))
    except ValueError as e:
        abort(make_response(jsonify(message=str(e)), 404))

