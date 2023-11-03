import collections

from gensim.models import KeyedVectors, Word2Vec

from backend.recommender.recommender.base_model import BaseModel
from backend.recommender.recommender.utils import RecallAtKLogger


class Word2VecModel(BaseModel):
    def __init__(self, embedding_file_path: str):
        self._embedding_file_path = embedding_file_path

    def _load_model(self, pretrained, hyperparameters):
        if pretrained:
            self._model = KeyedVectors.load_word2vec_format(self._embedding_file_path, binary=True)
            self._model.init_sims()
        else:
            data = [endpoint.bow for endpoint in self._endpoints]
            if hyperparameters:
                self._model = Word2Vec(data, **hyperparameters)
            else:
                self._model = Word2Vec(window=10, sg=1, hs=0,
                                       negative=10,  # for negative sampling
                                       alpha=0.03, min_alpha=0.0007,
                                       seed=14, vector_size=300)
                self._model.build_vocab(data, progress_per=200)
                self._model.train(data, total_examples=self._model.corpus_count, epochs=20)
                words = [item for list_words in data for item in list_words]
                self._vocab_count = collections.Counter(words)

    def _tune_hyperparameters(self, hyperparameters):
        logger = RecallAtKLogger(self._validation, self._test)
        Word2Vec(sentences=self._train, callbacks=[logger], **hyperparameters)
