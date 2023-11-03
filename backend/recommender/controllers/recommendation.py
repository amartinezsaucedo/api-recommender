from backend.recommender.recommender import FastTextModel, Word2VecModel
from backend.recommender.persistence.api import Endpoint
from backend.recommender.model.endpoint import Endpoint as EndpointModel


class RecommendationController:
    _DEFAULT_DESCRIPTION_VALUE = "No description provided"
    _models = {
        "fast_text": {
            "crawl-300d-2M-subword.bin": FastTextModel("recommender/recommender/pretrained/fast_text/crawl-300d-2M"
                                                       "-subword.bin")
        },
        "word2vec": {
            "SO_vectors_200.bin": Word2VecModel("recommender/recommender/pretrained/word2vec/SO_vectors_200.bin"),
            "word2vec-google-news-300.gz": Word2VecModel("recommender/recommender/pretrained/word2vec/word2vec"
                                                         "-google-news-300.gz")
        }
    }
    _instance = None
    _apis = []
    _initialized = False


    def initialize(self):
        if not self._initialized:
            self._apis = [EndpointModel(endpoint=endpoint.endpoint, description=endpoint.description, bow=endpoint.bow)
                         for endpoint in Endpoint.objects()]
            self._initialized = True

    def get_recommendations(self, query: str, model_algorithm: str, model_binary: str, k: int):
        if not (model_algorithm in self._models.keys() and model_binary in self._models[model_algorithm].keys()):
            raise ValueError("Model or algorithm not supported")
        if len(query.strip()) == 0:
            raise ValueError("A query string must be supplied")
        model = self._models[model_algorithm][model_binary]
        model.initialize(endpoints=self._apis, pretrained=True, hyperparameters=None)
        recommendations = model.get_predictions(query, k)
        recommendations = self._map_recommendations(recommendations)
        return recommendations

    def _map_recommendations(self, recommendations: list[Endpoint]):
        response = []
        for recommendation in recommendations:
            response.append({"endpoint": recommendation.endpoint, "description": recommendation.description})
        return response

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = RecommendationController()
        return cls._instance
