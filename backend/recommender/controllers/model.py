import glob
import os


class ModelController:
    _MODELS_DIRECTORY = "recommender/recommender/pretrained"

    def get_available_models(self):
        available_models = []
        for root_folder, subdirectories, files in os.walk(self._MODELS_DIRECTORY):
            for algorithm_name in subdirectories:
                models = []
                for file in glob.glob(f"{os.path.join(root_folder, algorithm_name)}/[!.]*"):
                    models.append(os.path.basename(file))
                available_models.append({"algorithm": algorithm_name, "models": models})

        return available_models
