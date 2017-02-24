import base64
import datetime
import json
import logging
import pykka
import requests
import time
import exceptions

from random import randint

logger = logging.getLogger('prophet-velen')

json_headers = {
    'content-type': 'application/json',
    'accept': 'application/json'
}


class StateEnum(object):
    PENDING = 'pending'
    TIMEOUT = 'timeout'
    FAILED = 'failed'


class Result(object):
    id = None
    status = None
    stdout = None
    stderr = None
    duration = None
    exitcode = None

    def __init__(self, result):
        try:
            self.id = result['id']
            self.status = result['status']
            self.stdout = result['stdout']
            self.stderr = result['stderr']
            self.duration = result['duration']
            self.exitcode = result['exitcode']
        except KeyError as ke:
            raise ValueError(ke.message)


class Config(object):
    id = None
    cpu = None
    mem = None
    disk = None
    platform = None
    count = None
    timeout = None
    problem = None
    code = None
    inputs = None
    outputs = None

    def __init__(self, config):
        self.cpu = config.get('cpu', 0.01)
        self.mem = config.get('mem', 32)
        self.disk = config.get('disk', 0.0)
        self.count = config.get('count', 1)
        self.timeout = config.get('timeout', 1000)

        try:
            self.platform = config['platform']
            self.problem = config['problem']
            self.code = config['code']
            self.inputs = config['inputs']
            self.outputs = config['outputs']
        except KeyError as ke:
            raise ValueError(ke.message)


class DockerConfig(Config):

    platform_image_mapping = {
        'java7': 'bittiger/java7',
        'shell': 'bittiger/shell'
    }

    def __init__(self, config):
        super(DockerConfig, self).__init__(config)
        self.id = self._generate_app_id(self.problem)

    @staticmethod
    def _generate_app_id(problem):
        return '%s-%s-%d' % (problem, datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S'), randint(0, 100))

    def get_spec(self):
        return {
            'id': self.id,
            'instances': self.count,
            'cpus': self.cpu,
            'mem': self.mem,
            'disk': self.disk,
            'container': {
                'type': 'DOCKER',
                'docker': {
                    'forcePullImage': False,
                    'image': self.platform_image_mapping[self.platform],
                    'network': None
                }
            },
            'cmd': "python /usr/local/bin/worker/basic.py test fd none 'hello' \"echo 'hello'\" 1 http://10.0.2.2:5000/v2/algorithm/%s False" % self.id
        }


class MarathonDispatcher(object):

    marathon_endpoint = None
    marathon_app_endpoint = None
    pending = None
    pending_limit = None

    def __init__(self, marathon_endpoint, pending_limit=5000):
        logger.info('starting marathon dispatcher')
        super(MarathonDispatcher, self).__init__()
        self.marathon_endpoint = marathon_endpoint
        self.marathon_app_endpoint = '%s/v2/apps' % self.marathon_endpoint
        self.pending = {}
        self.pending_limit = pending_limit

    def done(self, result_dict):
        """

        :param result_dict:
        :return:
        """
        result = Result(result_dict)
        print(result_dict)
        if result.id not in self.pending:

            #
            # - somehow we received a task not in the pending tasks
            #
            raise exceptions.RoutingException('received invalid task %s' % result.id)

        #
        # - the task is done, invoke callback and remove it from pending
        #
        task = self.pending.get(result.id)
        try:
            reply = requests.post(url=task.get('callback'), data=json.dumps(result_dict), headers=json_headers)

            if reply.status_code is 200:

                #
                # - callback executed successfully
                #
                self.pending.pop(result.id)

            else:
                # TODO - add retry logic for failing to call callback
                pass

        except Exception as e:

            #
            # - something went wrong with http request
            # TODO
            pass

    def dispatch(self, config_dict):

        #
        # - reached limit of pending evaluation tasks, reject incoming dispatch requests actively
        #
        if len(self.pending) is self.pending_limit:
            raise exceptions.MaximumPendingReachedException('limit of %d pending evaluation reached' % self.pending_limit)

        #
        # - must have a callback url from the http payload to notify frontend app when evaluation is done
        #
        if 'callback' not in config_dict:
            raise ValueError('callback url missing from incoming request')

        #
        # - mash incoming http payload into a docker configuration
        #
        task_config = DockerConfig(config_dict)

        #
        # - call marathon endpoint and ask for new task scheduling
        #
        reply = requests.post(url=self.marathon_app_endpoint, data=json.dumps(task_config.get_spec()), headers=json_headers)

        if reply.status_code is 201:

            #
            # - marathon started task successfully
            #
            logger.info('%s evaluation task created' % task_config.id)

            #
            # - put the evaluation task into pending hash
            #

            result = {
                task_config.id: {
                    'callback': config_dict.get('callback'),
                    'status': StateEnum.PENDING
                }
            }

            self.pending.update(result)

            return result

        else:

            #
            # - failed to start task (mostly because marathon is down), fail fast this evaluation request
            #
            raise exceptions.DispatchException('%s evaluation task creation failed')
