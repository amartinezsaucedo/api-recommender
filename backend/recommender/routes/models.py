from flask import Blueprint

from backend.recommender.controllers import ModelController

models = Blueprint('models', __name__)

controller = ModelController()


@models.get("/models")
def get_available_models():
    return controller.get_available_models()
