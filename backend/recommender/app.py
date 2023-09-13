from flask import Flask
from flask_cors import CORS

from backend.recommender.routes.recommendations import recommendations
from backend.recommender.routes.models import models
from backend.recommender.routes.dataset import dataset

app = Flask(__name__)

app.register_blueprint(recommendations, url_prefix="/api/v1")
app.register_blueprint(models, url_prefix="/api/v1")
app.register_blueprint(dataset, url_prefix="/api/v1")

CORS(app)

