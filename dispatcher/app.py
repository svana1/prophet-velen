import cfg.default as default_setting
import exceptions
import json
import os

from engine import (
    MarathonDispatcher
)

from flask import (
    Flask,
    request,
    jsonify
)
from werkzeug.exceptions import (
    BadRequest,
    NotFound,
    InternalServerError
)

app = Flask(__name__)

if 'ENV_CONFIG_FILE' in os.environ:
    app.config.from_envvar('ENV_CONFIG_FILE')
else:
    app.config.from_object(default_setting)

dispatcher = MarathonDispatcher(app.config['CONFIG_MARATHON_ENDPOINT'], app.config['CONFIG_MAXIMUM_PENDING_TASK'])


@app.route('/v2/algorithm', methods=['POST'])
def new_evaluation():
    payload = json.loads(request.data)
    if not payload:
        raise BadRequest(description='No payload found with incoming request')
    try:
        return jsonify(dispatcher.dispatch(payload)), 201
    except ValueError as ve:
        raise BadRequest(description='Missing field with incoming request %s' % ve.message)
    # except exceptions.DispatchException as de:
    #     raise InternalServerError(description=de.message)
    # except exceptions.MaximumPendingReachedException as mpre:
    #     raise InternalServerError(description=mpre.message)
    except Exception as e:
        raise InternalServerError(description=e.message)


@app.route('/v2/algorithm/<task_id>', methods=['DELETE'])
def evaluation_done(task_id):
    result = json.loads(request.data)
    if not result:
        raise BadRequest(description='No result found with incoming request')
    try:
        return jsonify(dispatcher.done(result)), 200
    except ValueError as ve:
        raise BadRequest(description='Missing field with incoming request %s' % ve.message)
    except exceptions.RoutingException as re:
        raise NotFound(description='Cannot find specified pending task %s' % re.message)
    except Exception as e:
        raise InternalServerError(e.message)


@app.route('/echo', methods=['POST'])
def echo():
    return request.data, 200


@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host=app.config['CONFIG_APPLICATION_HOST'], port=app.config['CONFIG_APPLICATION_PORT'])
