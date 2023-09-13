from flask import Blueprint, jsonify, abort, make_response

from backend.recommender.controllers.dataset import APIController

dataset = Blueprint('dataset', __name__)

controller = APIController()


@dataset.patch("/dataset")
def update_apis():
    try:
        return controller.update_apis()
    except Exception as e:
        abort(make_response(jsonify(message=str(e)), 500))


@dataset.get("/dataset")
def get_api_info():
    return jsonify({"commit": controller.get_api_information()})
