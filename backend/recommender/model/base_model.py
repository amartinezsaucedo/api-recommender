import json
import os

import numpy as np
from ray import tune as tuner
from ray.tune.schedulers import ASHAScheduler
from ray.tune.stopper import TrialPlateauStopper
from multiprocessing import cpu_count

from .singleton_metaclass import SingletonMeta
from .utils import recall_at_k, precision_at_k, ndcg_at_k, f1_score_at_k
from ..persistence.api import Endpoint


class BaseModel(metaclass=SingletonMeta):
    _model = None
    _vocab_count = None
    _endpoints: list[Endpoint]
    _test = None
    _train = None
    _validation = None
    _initialized = False

    def initialize(self, endpoints, pretrained, hyperparameters):
        if not self._initialized:
            self._endpoints = endpoints
            self._load_model(pretrained, hyperparameters)
            if pretrained:
                self._load_api_bows()
            self._initialized = True

    def initialize_evaluation(self, pretrained, hyperparameters):
        self._load_model(pretrained, hyperparameters)
        self._load_api_bows()

    def _load_model(self, pretrained, hyperparameters):
        pass

    def _load_api_bows(self):
        for endpoint in self._endpoints:
            endpoint.bow = [word for word in endpoint.bow if word in self._model.key_to_index]

    def train_test_split(self, queries_file_path, target_file_path, test_percentage=0.2, random_state=10,
                         save_test=True):
        random_state = np.random.RandomState(random_state)
        keys = [endpoint.id for endpoint in self._endpoints]
        random_state.shuffle(keys)
        train_keys = keys[:int(len(keys) * (1 - test_percentage))]
        test_keys = keys[-int(len(keys) * test_percentage):]
        train_apis_bows = dict()
        test_apis_bows = dict()
        train = []
        for key in train_keys:
            value = [endpoint for endpoint in self._endpoints if endpoint.id == key][0]
            train_apis_bows.update({key: value.endpoint})
            train.append(value.endpoint)
        if save_test:
            for key in test_keys:
                value = [endpoint for endpoint in self._endpoints if endpoint.id == key][0]
                api = value.endpoint
                test_apis_bows[api] = value.bow
            if not os.path.exists(f"{target_file_path}/test.json"):
                with open(f"{target_file_path}/test.json", "w") as fp:
                    json.dump(test_apis_bows, fp)
        with open(queries_file_path, "r") as file:
            validation = json.load(file)
        return train, test_apis_bows, validation

    def train_model(self, results_path, queries_file_path, target_file_path):
        self._train, self._test, self._validation = self.train_test_split(queries_file_path, target_file_path)
        asha_scheduler = ASHAScheduler(max_t=100, grace_period=10)
        stopping_criterion = TrialPlateauStopper(metric="recall_at_k", std=0.002)
        search_space = {
            "vector_size": tuner.grid_search([10, 100, 300, 1200, 1800, 2400, 3000]),
            "window": tuner.grid_search([2, 4, 8, 10]),
            "negative": tuner.grid_search([0, 1, 5, 10, 20]),
            "epochs": tuner.grid_search([10, 25, 35, 50]),
            "workers": cpu_count(),
            "sg": tuner.grid_search([0, 1]),
            "hs": tuner.grid_search([0, 1]),
        }
        analysis = tuner.run(
            self._tune_hyperparameters,
            metric="recall_at_k",
            mode="max",
            local_dir=results_path,
            scheduler=asha_scheduler,
            stop=stopping_criterion,
            verbose=1,
            num_samples=15,
            config=search_space,
        )
        results = analysis.best_dataframe
        results.to_csv(f"{results_path}/results.csv")

    def _tune_hyperparameters(self, hyperparameters):
        pass

    def get_predictions(self, query, k):
        query_bow = list([x for x in query.split() if x in self._model.key_to_index])
        predictions = []
        for endpoint in self._endpoints:
            if len(endpoint.bow) > 0:
                predictions.append((endpoint, self._model.n_similarity(query_bow, endpoint.bow)))
            else:
                predictions.append((endpoint, 0))
        return [api[0] for api in sorted(predictions, key=lambda item: -item[1])[0:k]]

    def evaluate(self, queries_file_path):
        with open(queries_file_path, "r") as file:
            validation = json.load(file)
        scores = {"recall": 0, "precision": 0, "ndcg": 0, "f1": 0}
        for item in validation:
            query_item = item["query"].split()
            ground_truth = item["results"]
            try:
                final_predictions = self.get_predictions(query_item, 10)
            except KeyError:
                pass
            else:
                recommendations = [item for item, distance in final_predictions]
                print(query_item)
                print(recommendations)
                scores["recall"] += recall_at_k(10, ground_truth, recommendations)[-1]
                scores["precision"] += precision_at_k(10, ground_truth, recommendations)[-1]
                scores["ndcg"] += ndcg_at_k(10, ground_truth, recommendations)[-1]
                scores["f1"] += f1_score_at_k(precision_at_k(10, ground_truth, recommendations),
                                              recall_at_k(10, ground_truth, recommendations))[-1]
        scores["recall"] /= len(validation)
        scores["precision"] /= len(validation)
        scores["ndcg"] /= len(validation)
        scores["f1"] /= len(validation)
        print(scores)

    def save_vocabulary_and_vectors(self, target_path):
        with open(f"{target_path}/vocab.txt", "w") as file:
            lines = [word + " " + str(vocab_obj) + '\n' for word, vocab_obj in self._vocab_count.most_common()]
            file.writelines(lines)
        with open(f"{target_path}/vectors.txt", "w") as file:
            words = list(w for w in self._model.index_to_key)
            lines = [word + " " + " ".join(map(str, self._model[word])) + '\n' for word in words]
            file.writelines(lines)
