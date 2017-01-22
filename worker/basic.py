import argparse
import base64
import json
import requests
import shutil
import tempfile
import threading
import time

from subprocess import (
    Popen,
    PIPE
)


class ResultEnum(object):
    PASSED = 'passed'
    FAILED = 'failed'
    TIMEOUT = 'over timelimit'


class Command(object):

    cmd = None
    process = None
    stdout = None
    stderr = None
    duration = None
    exitcode = None
    status = None

    def __init__(self, cmd):
        self.cmd = cmd

    def run(self, timeout, expected):

        def target():
            self.process = Popen(self.cmd, stdout=PIPE, stderr=PIPE, shell=True)
            self.stdout, self.stderr = self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        start = time.time()
        thread.join(timeout)
        end = time.time()
        self.duration = end - start

        if thread.is_alive():

            #
            # - passed preset timeout, terminate the process
            #
            self.process.terminate()
            self.status = ResultEnum.TIMEOUT
            thread.join()

        self.exitcode = self.process.returncode
        self.process = None

        #
        # - remove starting/tailing spaces and newlines
        #
        expected = expected.rstrip()
        self.stdout = self.stdout.rstrip()

        if self.stdout == expected:
            self.status = ResultEnum.PASSED
        else:
            self.status = ResultEnum.FAILED

    def result(self):
        return {
            'stdout': self.stdout,
            'stderr': self.stderr,
            'duration': self.duration,
            'exitcode': self.exitcode,
            'status': self.status
        }


if __name__ == '__main__':
    #
    # - setup commandline arguments
    #
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='id of the task for tracking purpose')
    parser.add_argument('code', help='source code to execute')
    parser.add_argument('inputs', help='input as test case')
    parser.add_argument('outputs', help='exepected output')
    parser.add_argument('cmd', help='command line argument to invoke for test case')
    parser.add_argument('timeout', help='maximum time allowed to run the program')
    parser.add_argument('callback', help='callback endpoint')
    parser.add_argument('base64', help='is code, inputs, outputs base64 encoded')

    args = parser.parse_args()
    id = args.id
    code = args.code
    inputs = args.inputs
    outputs = args.outputs
    cmd = args.cmd
    timeout = float(args.timeout)
    callback = args.callback

    tmp = tempfile.mkdtemp()

    command = Command(cmd)
    command.run(timeout, outputs)
    result = command.result()
    result.update({
        'id': id,
    })

    if callback:
        requests.delete(url=callback, data=json.dumps(result))
