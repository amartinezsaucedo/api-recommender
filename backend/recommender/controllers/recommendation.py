from backend.recommender.extractor.extract import extract_oapi_data
from backend.recommender.model import FastTextModel, Word2VecModel
from backend.recommender.processer.transform import transform_oapi_data


class RecommendationController:
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

    def get_recommendations(self, query: str, model_algorithm: str, model_binary: str):
        model = self._models[model_algorithm][model_binary]
        model.initialize(api_info=self.api_data_info, bow_apis=self.preprocessed_api_data,
                         pretrained=True, hyperparameters=None)
        return model.get_predictions(query)
