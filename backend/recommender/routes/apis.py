from flask import Blueprint

from backend.recommender.controllers.api import APIController

apis = Blueprint('apis', __name__)

controller = APIController()


@apis.patch
def update_apis():
    return controller.update_apis()
