import os
import shutil

from backend.recommender.extractor.extract import extract_oapi_data, DATA_FILENAME, APIS_TARGET_FOLDER_NAME
from backend.recommender.processer.transform import transform_oapi_data


class APIController:
    def update_apis(self):
        os.remove(DATA_FILENAME)
        shutil.rmtree(APIS_TARGET_FOLDER_NAME)
        api_data = extract_oapi_data()
        (self.preprocessed_api_data, self.api_data_info) = transform_oapi_data(api_data)

