import os
import redis

from config import (
    config
)

from flask import (
    Flask,
    jsonify,
    request
)

from model import (
    EvaluationResult,
    EvaluationRequest,
    States
)

from redis import (
    ConnectionError,
    BusyLoadingError
)

from werkzeug.exceptions import (
    BadRequest,
    NotFound,
    InternalServerError
)

version = '0.0.1'
app = Flask(__name__)
env = os.environ['ENVIRONMENT']
app.config.from_object(config[env])
rs = redis.Redis(host=app.config['REDIS_ENDPOINT'], port=app.config['REDIS_PORT'])


image_mapping = {
    'java': 'unclebarney/oj-java',
    'python': 'unclebarney/oj-python'
}


@app.route('/v1/eval', methods=['POST'])
def _create_evaluation():
    try:
        request_dict = request.get_json()

        if not request_dict:
            raise BadRequest(jsonify({
                'error': 'Cannot find json payload from incoming request'
            }))

        eval_request = EvaluationRequest.parse_from_dict(request_dict)
        image = image_mapping[eval_request.platform]

        # - TODO

        rs.hset(eval_request.id, 'config', request_dict)
        rs.hset(eval_request.id, 'status', States.EVALUATING)
        rs.expire(eval_request.id, 3600)
        return jsonify({
            'id': request_dict.id,
            'status': States.EVALUATING
        }), 200

    except KeyError as ke:
        return BadRequest(jsonify({
            'error': 'Incoming data is missing or has wrong property: %s' % ke.message
        }))


@app.route('/v1/eval/<uuid:request_id>', methods=['GET'])
def _get_evaluation(request_id):
    try:
        if not request_id:
            raise BadRequest('Request ID cannot be empty')
        request_status = rs.hget(request_id, 'status')
        if not request_status:
            raise NotFound('Evaluation with ID %s not found' % request_id)
        return jsonify({
            'id': request_id,
            'status': request_status
        }), 200
    except (ConnectionError, BusyLoadingError) as ce:
        return InternalServerError(jsonify({
            'error': 'Unable to connect to database'
        }))


@app.route('/v1/eval/<uuid:request_id>/result', methods=['POST'])
def _process_evaluation_result(request_id):
    try:
        result_dict = request.get_json()

        if not result_dict:
            raise BadRequest(jsonify({
                'error': 'Cannot find json payload from incoming request'
            }))

        if not request_id:
            raise BadRequest(jsonify({
                'error': 'Request ID cannot be empty'
            }))

        request_data = rs.hgetall(request_id)
        if not request_data:
            # - TODO we get a callback invoke from worker after long time, log that
            pass

        # - TODO

    except (ConnectionError, BusyLoadingError) as ce:
        return InternalServerError(jsonify({
            'error': 'Unable to connect to database'
        }))


@app.route('/v1/health')
def _health():
    try:
        redis_info = rs.info()
        return jsonify({
            'redis': redis_info,
            'version': version
        }), 200
    except (ConnectionError, BusyLoadingError) as ce:
        return InternalServerError(jsonify({
            'redis': 'Unable to connect to database',
            'version': version
        }))
