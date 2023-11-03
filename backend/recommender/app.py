from dotenv import dotenv_values
from flask import Flask, current_app
from flask_cors import CORS
from flask_mongoengine import MongoEngine

from backend.recommender.controllers import APIController
from backend.recommender.routes.recommendations import recommendations, controller as recommendations_controller
from backend.recommender.routes.models import models
from backend.recommender.routes.dataset import dataset


app = Flask(__name__)

configuration = dotenv_values(".env")
app.config['MONGODB_SETTINGS'] = {
    "db": configuration["DB_NAME"],
    "host": configuration["ATLAS_URI"]
}

db = MongoEngine(app)

app.register_blueprint(recommendations, url_prefix="/api/v1")
app.register_blueprint(models, url_prefix="/api/v1")
app.register_blueprint(dataset, url_prefix="/api/v1")

CORS(app)

with app.app_context():
    api_controller = APIController()
    api_controller.clean_tasks(current_app)
    recommendations_controller.initialize()
