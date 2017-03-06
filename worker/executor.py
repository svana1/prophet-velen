import base64
import boto3
import json
import logging
import os
import requests
import shlex
import subprocess
import tempfile
import time

from botocore.exceptions import (
    BotoCoreError,
    ClientError
)

from retrying import (
    retry,
    RetryError
)

from threading import (
    Timer
)

logger = logging.getLogger('worker')


class Executor(object):

    version = '0.0.1'

    id = None
    base64_code = None
    driver_link = None
    runtime_limit = 10.0  # - runtime limit in seconds
    callback_url = None
    inputs = []
    outputs = []
    result = None
    s3_base = None
    s3 = None

    dir_path = None

    def __init__(self):
        self._parse_environ()
        try:
            self.s3 = boto3.client('s3')
            self.dir_path = tempfile.mkdtemp()

            for index, filename in self.inputs:
                self.s3.meta.client.download_file(self.s3_base, filename, '%s/input/%d.txt' % (self.dir_path, index))

            for index, filename in self.outputs:
                self.s3.meta.client.download_file(self.s3_base, filename, '%s/output/%d.txt' % (self.dir_path, index))

            self.s3.meta.client.download_file(
                self.s3_base,
                self.driver_link,
                '%s/%s' % (self.dir_path, os.path.basename(self.driver_link))
            )
        except ClientError as ce:
            logger.error('Error loading files from S3: %s' % ce.message)
            raise ce
        except BotoCoreError as bce:
            logger.error('Error connecting to aws: %s' % bce.message)
            raise bce

        with open('%s/code', 'w+') as f:
            f.write(base64.b64decode(self.base64_code))

    def _parse_environ(self):
        """
        Parse environment variables and extract out input s3 links, output s3 links, driver s3 link, runtime limit, and
        base64 encoded code.

        environment variable mappings:
        * S3_BASE -> s3 base url
        * INPUTS -> input series
        * OUTPUTS -> input series
        * DRIVER -> code driver S3 link
        * RUNTIME_LIMIT -> runtime limit
        * CODE -> base64 encoded code
        * DISPATCHER_URL -> dispatcher callback url
        * ID -> id of the evaluation request

        Raises:
            KeyError: if required environment variables don't exist
        """
        try:
            env = os.environ
            self.id = env['ID']
            self.s3_base = env['S3_BASE']
            self.base64_code = env['CODE']
            self.driver_link = env['DRIVER']
            self.runtime_limit = float(env['RUNTIME_LIMIT'])
            self.callback_url = env['DISPATCHER_URL']
            self.inputs = env['INPUTS'].split(',')
            self.outputs = env['OUTPUTS'].split(',')
        except KeyError as ke:
            logger.error('Missing required environment variable: %s' % ke.message)
            raise ke

    def construct(self):
        """
        Function that subclasses need to implement that takes in input, output, driver, and code and construct an
        executable format
        """
        raise NotImplementedError

    def run(self, command):
        """
        Run command through subprocess with a timeout.

        Args:
            command: String type. Command to execute, such as `javac Main.java && java`
        """
        proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.dir_path)

        def kill_proc(p):
            p.kill()

        timer = Timer(self.runtime_limit, kill_proc, [proc])
        start = time.time()
        timer.start()
        stdout, stderr = proc.communicate()
        end = time.time()
        timer.cancel()

        returncode = proc.returncode

        if returncode == 0:
            state = 'pass'
        elif returncode == -9:
            state = 'timeout'
        else:
            state = 'fail'

        return {
            'id': self.id,
            'status': state,
            'stdout': stdout,
            'stderr': stderr,
            'exitcode': returncode,
            'duration': end - start
        }

    def report(self, result):

        @retry(stop_max_delay=10000, stop_max_attempt_number=10, wait_fixed=1000)
        def _http_post_with_retry(callback_url, payload):
            """
            Send result as payload to target callback_url using HTTP Post method.
            This method will automatically retry, up to 10 times, at 1 second inteval, maximum retry time is 10 seconds

            Args:
                callback_url: URL type. Target endpoint to send data back
                payload: Dict type. Dictionary object containing the evaluation result
            """
            response = requests.post(url=callback_url, data=json.dumps(payload))
            code = response.status_code
            assert code == 200, 'Failed to talk to callback endpoint (HTTP %d)' % code

        try:
            _http_post_with_retry(self.callback_url, result)
        except RetryError as re:
            logger.error('Maximum retried reached unable to ping back: %s' % re.message)
        except Exception as e:
            logger.error('Unknown failure case: %s' % e.message)
