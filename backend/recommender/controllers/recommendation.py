from backend.recommender.extractor.extract import extract_oapi_data
from backend.recommender.model import FastTextModel, Word2VecModel
from backend.recommender.processer.transform import transform_oapi_data, API_INFO_FILE


class RecommendationController:
    _DEFAULT_DESCRIPTION_VALUE = "No description provided"
    _models = {
        "fast_text": {
            "crawl-300d-2M-subword.bin": FastTextModel("backend/recommender/model/pretrained/fast_text/crawl-300d-2M"
                                                       "-subword.bin")
        },
        "word2vec": {
            "SO_vectors_200.bin": Word2VecModel("backend/recommender/model/pretrained/word2vec/SO_vectors_200.bin"),
            "word2vec-google-news-300.gz": Word2VecModel("backend/recommender/model/pretrained/word2vec/word2vec"
                                                         "-google-news-300.gz")
        }
    }

    def __init__(self):
        api_data = extract_oapi_data()
        (self.preprocessed_api_data, self.api_data_info) = transform_oapi_data(api_data)

    def get_recommendations(self, query: str, model_algorithm: str, model_binary: str, k: int):
        if not (model_algorithm in self._models.keys() and model_binary in self._models[model_algorithm].keys()):
            raise ValueError("Model or algorithm not supported")
        if len(query.strip()) == 0:
            raise ValueError("A query string must be supplied")
        model = self._models[model_algorithm][model_binary]
        model.initialize(api_info=self.api_data_info, bow_apis=self.preprocessed_api_data,
                         pretrained=True, hyperparameters=None)
        recommendations = model.get_predictions(query, k)
        recommendations = self._add_api_description(recommendations)
        return recommendations

    def _add_api_description(self, recommendations):
        response = []
        for recommendation in recommendations:
            response.append({"endpoint": recommendation, "description": self.find_description_for_api(recommendation)})
        return response

    def find_description_for_api(self, recommendation):
        api = [api_info for api_info in list(self.api_data_info.values()) if api_info[0] == recommendation]
        if len(api):
            return api[0][-1]
        return self._DEFAULT_DESCRIPTION_VALUE
