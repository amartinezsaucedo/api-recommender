import os
import shutil
import threading
import time
import uuid
from datetime import datetime

from backend.recommender.extractor.extract import extract_oapi_data, DATA_FILENAME, APIS_TARGET_FOLDER_NAME, \
    DATASET_COMMIT_FILENAME
from backend.recommender.persistence.api import Endpoint
from backend.recommender.processer.transform import transform_oapi_data


class APIController:
    _tasks = {}

    def update_apis(self):
        try:
            os.remove(DATA_FILENAME)
        except OSError:
            pass
        shutil.rmtree(APIS_TARGET_FOLDER_NAME)
        Endpoint.objects.delete()
        endpoints = extract_oapi_data()
        endpoints = transform_oapi_data(endpoints)
        Endpoint.objects.insert(endpoints)


    def get_api_information(self) -> str:
        with open(DATASET_COMMIT_FILENAME) as file:
            dataset_info = file.readlines()[0]
        return dataset_info

    def clean_tasks(self, current_app):
        def clean_old_tasks():
            while True:
                five_min_ago = datetime.timestamp(datetime.utcnow()) - 5 * 60
                self._tasks = {task_id: task for task_id, task in self._tasks.items()
                               if 'completion_timestamp' not in task or task['completion_timestamp'] > five_min_ago}
                time.sleep(60)

        if not current_app.config['TESTING']:
            thread = threading.Thread(target=clean_old_tasks)
            thread.start()

    def get_task(self, task_id):
        return self._tasks.get(task_id)

    def get_tasks(self):
        return self._tasks

    def set_value(self, task_id, key, value):
        self._tasks[task_id][key] = value

    def create_task(self, task_call, app, request):
        task_id = uuid.uuid4().hex
        self._tasks[task_id] = {'task_thread': threading.Thread(target=task_call, args=(task_id, app, request.environ))}
        self._tasks[task_id]['task_thread'].start()
        return task_id
