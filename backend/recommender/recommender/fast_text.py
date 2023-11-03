from gensim.models import FastText
from gensim.models.fasttext import load_facebook_vectors

from backend.recommender.recommender.base_model import BaseModel
from backend.recommender.recommender.utils import RecallAtKLogger


class FastTextModel(BaseModel):
    def __init__(self, embedding_file_path: str):
        self._embedding_file_path = embedding_file_path

    def _load_model(self, pretrained, hyperparameters):
        if pretrained:
            self._model = load_facebook_vectors(self._embedding_file_path)
            self._model.init_sims()
        elif hyperparameters:
            self._model = FastText([endpoint.bow for endpoint in self._endpoints], **hyperparameters)

    def _tune_hyperparameters(self, hyperparameters):
        logger = RecallAtKLogger(self._validation, self._test)
        FastText(sentences=self._train, callbacks=[logger], **hyperparameters)
