import json
import os
import requests
import shlex
import subprocess
import time

from retrying import (
    retry,
    RetryError
)
from threading import (
    Timer
)


class Executor(object):

    base64_code = None
    driver_link = None
    runtime_limit = 10.0  # - runtime limit in seconds
    callback_url = None
    input_output_link_paris = []

    def __init__(self):
        self._parse_environ()

    def _parse_environ(self):
        """
        Parse environment variables and extract out input s3 links, output s3 links, driver s3 link, runtime limit, and
        base64 encoded code.

        environment variable mappings:
        * OJ_TEST_COUNT -> # of test cases
        * OJ_INPUT_0 -> input series 0 S3 link
        * OJ_OUTPUT_0 -> input series 0 S3 link
        * OJ_DRIVER -> code driver S3 link
        * OJ_RUNTIME_LIMIT -> runtime limit
        * OJ_CODE -> base64 encoded code
        * OJ_DISPATCHER_URL -> dispatcher callback url

        Raises:
            KeyError: if required environment variables don't exist
        """
        env = os.environ
        self.base64_code = env['OJ_CODE']
        self.driver_link = env['OJ_DRIVER']
        self.runtime_limit = float(env['OJ_RUNTIME_LIMIT'])
        self.callback_url = env['OJ_DISPATCHER_URL']
        test_count = env['OJ_TEST_COUNT']
        for i in range(test_count):
            self.input_output_link_paris.append({
                'input': os.environ['OJ_INPUT_{0}'.format(i)],
                'output': os.environ['OJ_OUTPUT_{0}'.format(i)]
            })

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

        Returns:
            returncode: Int type. Exit code of the command
            stdout: String type. UTF-8 encoded stdout of the command
            stderr: String type. UTF-8 encoded stderr of the command
            runtime: Float type. The actual runtime of the command
        """
        proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        def kill_proc(p):
            p.kill()

        timer = Timer(self.runtime_limit, kill_proc, [proc])
        start = time.time()
        timer.start()
        stdout, stderr = proc.communicate()
        end = time.time()
        timer.cancel()
        return proc.returncode, stdout.decode('utf-8'), stderr.decode('utf-8'), end - start

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
            # - TODO add log
            pass
        except Exception as e:
            # - TODO add log
            pass
