#!flask/bin/python
import requests
from flask import Flask, jsonify, make_response, url_for

from service.config import configure_app
from service.utils import get_instance_folder_path

app = Flask(__name__, instance_path=get_instance_folder_path(),
            instance_relative_config=True)
configure_app(app)
SETLIST_FM_API_KEY_ = app.config['SETLIST_FM_API_KEY']


# sample code: https://gist.github.com/shivam5992/8451692
# from https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
# flask resources https://github.com/miguelgrinberg


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'message': error.description}), 404)


@app.errorhandler(500)
def tech_error(error):
    return make_response(jsonify({'error': 'Technical error.', 'message': error.description}), 500)


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run(debug=True, host=app.config['SETLIST_HOST'], port=app.config['SETLIST_PORT'])
