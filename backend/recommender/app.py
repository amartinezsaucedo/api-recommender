from flask import Flask, current_app
from flask_cors import CORS

from backend.recommender.controllers import APIController
from backend.recommender.routes.recommendations import recommendations
from backend.recommender.routes.models import models
from backend.recommender.routes.dataset import dataset

app = Flask(__name__)

app.register_blueprint(recommendations, url_prefix="/api/v1")
app.register_blueprint(models, url_prefix="/api/v1")
app.register_blueprint(dataset, url_prefix="/api/v1")

CORS(app)

api_controller = APIController()

with app.app_context():
    api_controller.clean_tasks(current_app)
