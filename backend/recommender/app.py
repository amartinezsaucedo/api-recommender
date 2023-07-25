from flask import Flask

from backend.recommender.routes.recommendations import recommendations
from backend.recommender.routes.models import models
from backend.recommender.routes.apis import apis

app = Flask(__name__)

app.register_blueprint(recommendations)
app.register_blueprint(models)
app.register_blueprint(apis)


