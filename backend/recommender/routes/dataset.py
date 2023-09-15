from datetime import datetime
from functools import wraps

from flask import Blueprint, jsonify, abort, make_response, request, current_app, url_for
from werkzeug.exceptions import HTTPException, InternalServerError

from backend.recommender.controllers.dataset import APIController

dataset = Blueprint('dataset', __name__)

controller = APIController()


@dataset.get("/dataset")
def get_api_info():
    return jsonify({"commit": controller.get_api_information()})


@dataset.get("/tasks")
def get_task_status():
    task_id = request.args.get("task_id")
    task = controller.get_task(task_id)
    if task is None:
        abort(404)
    if 'return_value' not in task:
        return '', 202, {'Location': url_for('dataset.get_task_status', task_id=task_id)}
    return task['return_value']


def async_api(wrapped_function):
    @wraps(wrapped_function)
    def new_function(*args, **kwargs):
        def task_call(task_id, flask_app, environ):
            with flask_app.request_context(environ):
                try:
                    controller.set_value(task_id, "return_value", wrapped_function(*args, **kwargs))
                except HTTPException as e:
                    controller.set_value(task_id, "return_value", current_app.handle_http_exception(e))
                except Exception:
                    controller.set_value(task_id, "return_value", InternalServerError())
                finally:
                    controller.set_value(task_id, "completion_timestamp", datetime.timestamp(datetime.utcnow()))

        new_task_id = controller.create_task(task_call, current_app._get_current_object(), request)
        return 'Accepted', 202, {'Location': url_for('dataset.get_task_status', task_id=new_task_id)}

    return new_function


@dataset.patch("/dataset")
@async_api
def update_apis():
    try:
        controller.update_apis()
        return make_response(jsonify(message="Complete"), 200)
    except Exception as e:
        abort(make_response(jsonify(message=str(e)), 500))
