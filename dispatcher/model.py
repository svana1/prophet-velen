import time


class States(object):
    EVALUATING = 'pending'
    FAIL = 'fail'
    PASS = 'pass'
    TIMEOUT = 'timeout'


class EvaluationResult(object):

    id = None
    status = None
    stdout = None
    stderr = None
    exitcode = None
    duration = None

    def __init__(self, request_id, status, stdout, stderr, exitcode, duration):
        self.id = request_id
        self.status = status
        self.stdout = stdout
        self.stderr = stderr
        self.exitcode = exitcode
        self.duration = duration

    @property
    def id(self):
        """
        Gets the request_id of this EvaluationResult.
        UUID identifying a evaluation request

        :return: The request_id of this EvaluationResult.
        :rtype: str
        """
        return self.id

    @id.setter
    def id(self, request_id):
        """
        Sets the request_id of this EvaluationResult.
        UUID identifying a evaluation request

        :param request_id: The request_id of this EvaluationResult.
        :type request_id: str
        """
        self.id = request_id

    @property
    def status(self):
        """
        Gets the status of this EvaluationResult.
        Status of the evaluation

        :return: The status of this EvaluationResult.
        :rtype: EvaluationState
        """
        return self.status

    @status.setter
    def status(self, status):
        """
        Sets the status of this EvaluationResult.
        Status of the evaluation

        :param status: The status of this EvaluationResult.
        :type status: EvaluationState
        """
        self.status = status

    @property
    def stdout(self):
        """
        Gets the stdout of this EvaluationResult.
        Standard out from code execution

        :return: The stdout of this EvaluationResult.
        :rtype: str
        """
        return self.stdout

    @stdout.setter
    def stdout(self, stdout):
        """
        Sets the stdout of this EvaluationResult.
        Standard out from code execution

        :param stdout: The stdout of this EvaluationResult.
        :type stdout: str
        """

        self.stdout = stdout

    @property
    def stderr(self):
        """
        Gets the stderr of this EvaluationResult.
        Standard error from code execution

        :return: The stderr of this EvaluationResult.
        :rtype: str
        """
        return self.stderr

    @stderr.setter
    def stderr(self, stderr):
        """
        Sets the stderr of this EvaluationResult.
        Standard error from code execution

        :param stderr: The stderr of this EvaluationResult.
        :type stderr: str
        """

        self.stderr = stderr

    @property
    def exitcode(self):
        """
        Gets the exitcode of this EvaluationResult.
        Exit code from evaluation payload process

        :return: The exitcode of this EvaluationResult.
        :rtype: str
        """
        return self.exitcode

    @exitcode.setter
    def exitcode(self, exitcode):
        """
        Sets the exitcode of this EvaluationResult.
        Exit code from evaluation payload process

        :param exitcode: The exitcode of this EvaluationResult.
        :type exitcode: str
        """

        self.exitcode = exitcode

    @property
    def duration(self):
        """
        Gets the duration of this EvaluationResult.
        Total evaluation duration of the problem

        :return: The duration of this EvaluationResult.
        :rtype: int
        """
        return self.duration

    @duration.setter
    def duration(self, duration):
        """
        Sets the duration of this EvaluationResult.
        Total evaluation duration of the problem

        :param duration: The duration of this EvaluationResult.
        :type duration: int
        """

        self.duration = duration


class EvaluationRequest(object):

    def __init__(self, request_id, platform, runtime_limit, s3_base_link, input_links, output_links, driver_link, code, callback):
        self.id = request_id
        self.platform = platform
        self.runtime = runtime_limit
        self.s3_base = s3_base_link
        self.inputs = input_links
        self.outputs = output_links
        self.driver = driver_link
        self.code = code
        self.timestamp = time.time()
        self.callback = callback

    @property
    def id(self):
        """
        Gets the request_id of this EvaluationRequest.
        UUID identifying a evaluation request

        :return: The request_id of this EvaluationRequest.
        :rtype: str
        """
        return self.id

    @id.setter
    def id(self, request_id):
        """
        Sets the request_id of this EvaluationRequest.
        UUID identifying a evaluation request

        :param request_id: The request_id of this EvaluationRequest.
        :type request_id: str
        """
        self.id = request_id

    @property
    def platform(self):
        """
        Gets the platform of this EvaluationRequest.
        Runtime platform for evaluation, such as Java, Python, etc

        :return: The platform of this EvaluationRequest.
        :rtype: EvaluationPlatform
        """
        return self.platform

    @platform.setter
    def platform(self, platform):
        """
        Sets the platform of this EvaluationRequest.
        Runtime platform for evaluation, such as Java, Python, etc

        :param platform: The platform of this EvaluationRequest.
        :type platform: EvaluationPlatform
        """
        self.platform = platform

    @property
    def runtime(self):
        """
        Gets the runtime_limit of this EvaluationRequest.
        Total evaluation duration allowed for the problem

        :return: The runtime_limit of this EvaluationRequest.
        :rtype: int
        """
        return self.runtime

    @runtime.setter
    def runtime(self, runtime_limit):
        """
        Sets the runtime_limit of this EvaluationRequest.
        Total evaluation duration allowed for the problem

        :param runtime_limit: The runtime_limit of this EvaluationRequest.
        :type runtime_limit: int
        """
        self.runtime = runtime_limit

    @property
    def inputs(self):
        """
        Gets the input_links of this EvaluationRequest.

        :return: The input_links of this EvaluationRequest.
        :rtype: List[str]
        """
        return self.inputs

    @inputs.setter
    def inputs(self, input_links):
        """
        Sets the input_links of this EvaluationRequest.

        :param input_links: The input_links of this EvaluationRequest.
        :type input_links: List[str]
        """
        self.inputs = input_links

    @property
    def outputs(self):
        """
        Gets the output_link of this EvaluationRequest.

        :return: The output_link of this EvaluationRequest.
        :rtype: List[str]
        """
        return self.outputs

    @outputs.setter
    def outputs(self, output_links):
        """
        Sets the output_link of this EvaluationRequest.

        :param output_links: The output_link of this EvaluationRequest.
        :type output_links: List[str]
        """
        self.outputs = output_links

    @property
    def driver(self):
        """
        Gets the driver_link of this EvaluationRequest.
        S3 link pointing to the driver program that parses input and output files to language specific format

        :return: The driver_link of this EvaluationRequest.
        :rtype: str
        """
        return self.driver

    @driver.setter
    def driver(self, driver_link):
        """
        Sets the driver_link of this EvaluationRequest.
        S3 link pointing to the driver program that parses input and output files to language specific format

        :param driver_link: The driver_link of this EvaluationRequest.
        :type driver_link: str
        """
        self.driver = driver_link

    @property
    def code(self):
        """
        Gets the code of this EvaluationRequest.
        base64 encoded code string from user

        :return: The code of this EvaluationRequest.
        :rtype: ByteArray
        """
        return self.code

    @code.setter
    def code(self, code):
        """
        Sets the code of this EvaluationRequest.
        base64 encoded code string from user

        :param code: The code of this EvaluationRequest.
        :type code: ByteArray
        """
        self.code = code

    @property
    def timestamp(self):
        return self.timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self.timestamp = timestamp

    @property
    def callback(self):
        return self.callback

    @callback.setter
    def callback(self, callback):
        self.callback = callback

    @property
    def s3_base(self):
        return self.s3_base

    @s3_base.setter
    def s3_base(self, s3_base):
        self.s3_base = s3_base

    @staticmethod
    def parse_from_dict(dict_obj):
        request_id = dict_obj['request_id'],
        platform = dict_obj['platform'],
        s3_base = dict_obj['s3_base'],
        runtime_limit = dict_obj.get('runtime_limit', 5.0)
        input_links = dict_obj['input_links']
        output_links = dict_obj['output_links']
        driver_link = dict_obj['driver_link']
        code = dict_obj['code']
        callback = dict_obj['callback']

        return EvaluationRequest(request_id, platform, runtime_limit, s3_base, input_links, output_links, driver_link, code, callback)
