from __future__ import absolute_import


class EvaluationResult(object):

    _request_id = None
    _status = None
    _stdout = None
    _stderr = None
    _exitcode = None
    _duration = None

    def __init__(self, request_id, status, stdout, stderr, exitcode, duration):
        self._request_id = request_id
        self._status = status
        self._stdout = stdout
        self._stderr = stderr
        self._exitcode = exitcode
        self._duration = duration

    @property
    def request_id(self):
        """
        Gets the request_id of this EvaluationResult.
        UUID identifying a evaluation request

        :return: The request_id of this EvaluationResult.
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """
        Sets the request_id of this EvaluationResult.
        UUID identifying a evaluation request

        :param request_id: The request_id of this EvaluationResult.
        :type request_id: str
        """
        self._request_id = request_id

    @property
    def status(self):
        """
        Gets the status of this EvaluationResult.
        Status of the evaluation

        :return: The status of this EvaluationResult.
        :rtype: EvaluationState
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this EvaluationResult.
        Status of the evaluation

        :param status: The status of this EvaluationResult.
        :type status: EvaluationState
        """
        self._status = status

    @property
    def stdout(self):
        """
        Gets the stdout of this EvaluationResult.
        Standard out from code execution

        :return: The stdout of this EvaluationResult.
        :rtype: str
        """
        return self._stdout

    @stdout.setter
    def stdout(self, stdout):
        """
        Sets the stdout of this EvaluationResult.
        Standard out from code execution

        :param stdout: The stdout of this EvaluationResult.
        :type stdout: str
        """

        self._stdout = stdout

    @property
    def stderr(self):
        """
        Gets the stderr of this EvaluationResult.
        Standard error from code execution

        :return: The stderr of this EvaluationResult.
        :rtype: str
        """
        return self._stderr

    @stderr.setter
    def stderr(self, stderr):
        """
        Sets the stderr of this EvaluationResult.
        Standard error from code execution

        :param stderr: The stderr of this EvaluationResult.
        :type stderr: str
        """

        self._stderr = stderr

    @property
    def exitcode(self):
        """
        Gets the exitcode of this EvaluationResult.
        Exit code from evaluation payload process

        :return: The exitcode of this EvaluationResult.
        :rtype: str
        """
        return self._exitcode

    @exitcode.setter
    def exitcode(self, exitcode):
        """
        Sets the exitcode of this EvaluationResult.
        Exit code from evaluation payload process

        :param exitcode: The exitcode of this EvaluationResult.
        :type exitcode: str
        """

        self._exitcode = exitcode

    @property
    def duration(self):
        """
        Gets the duration of this EvaluationResult.
        Total evaluation duration of the problem

        :return: The duration of this EvaluationResult.
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """
        Sets the duration of this EvaluationResult.
        Total evaluation duration of the problem

        :param duration: The duration of this EvaluationResult.
        :type duration: int
        """

        self._duration = duration
