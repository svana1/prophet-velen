from __future__ import absolute_import


class EvaluationRequest(object):

    _request_id = None
    _platform = None
    _runtime_limit = 0
    _input_links = None
    _output_links = None
    _driver_link = None
    _code = None

    def __init__(self, request_id, platform, runtime_limit, input_links, output_links, driver_link, code):
        self._request_id = request_id
        self._platform = platform
        self._runtime_limit = runtime_limit
        self._input_links = input_links
        self._output_links = output_links
        self._driver_link = driver_link
        self._code = code

    @property
    def request_id(self):
        """
        Gets the request_id of this EvaluationRequest.
        UUID identifying a evaluation request

        :return: The request_id of this EvaluationRequest.
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """
        Sets the request_id of this EvaluationRequest.
        UUID identifying a evaluation request

        :param request_id: The request_id of this EvaluationRequest.
        :type request_id: str
        """
        self._request_id = request_id

    @property
    def platform(self):
        """
        Gets the platform of this EvaluationRequest.
        Runtime platform for evaluation, such as Java, Python, etc

        :return: The platform of this EvaluationRequest.
        :rtype: EvaluationPlatform
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """
        Sets the platform of this EvaluationRequest.
        Runtime platform for evaluation, such as Java, Python, etc

        :param platform: The platform of this EvaluationRequest.
        :type platform: EvaluationPlatform
        """
        self._platform = platform

    @property
    def runtime_limit(self):
        """
        Gets the runtime_limit of this EvaluationRequest.
        Total evaluation duration allowed for the problem

        :return: The runtime_limit of this EvaluationRequest.
        :rtype: int
        """
        return self._runtime_limit

    @runtime_limit.setter
    def runtime_limit(self, runtime_limit):
        """
        Sets the runtime_limit of this EvaluationRequest.
        Total evaluation duration allowed for the problem

        :param runtime_limit: The runtime_limit of this EvaluationRequest.
        :type runtime_limit: int
        """
        self._runtime_limit = runtime_limit

    @property
    def input_links(self):
        """
        Gets the input_links of this EvaluationRequest.

        :return: The input_links of this EvaluationRequest.
        :rtype: List[str]
        """
        return self._input_links

    @input_links.setter
    def input_links(self, input_links):
        """
        Sets the input_links of this EvaluationRequest.

        :param input_links: The input_links of this EvaluationRequest.
        :type input_links: List[str]
        """
        self._input_links = input_links

    @property
    def output_links(self):
        """
        Gets the output_link of this EvaluationRequest.

        :return: The output_link of this EvaluationRequest.
        :rtype: List[str]
        """
        return self._output_links

    @output_links.setter
    def output_links(self, output_links):
        """
        Sets the output_link of this EvaluationRequest.

        :param output_links: The output_link of this EvaluationRequest.
        :type output_links: List[str]
        """
        self._output_links = output_links

    @property
    def driver_link(self):
        """
        Gets the driver_link of this EvaluationRequest.
        S3 link pointing to the driver program that parses input and output files to language specific format

        :return: The driver_link of this EvaluationRequest.
        :rtype: str
        """
        return self._driver_link

    @driver_link.setter
    def driver_link(self, driver_link):
        """
        Sets the driver_link of this EvaluationRequest.
        S3 link pointing to the driver program that parses input and output files to language specific format

        :param driver_link: The driver_link of this EvaluationRequest.
        :type driver_link: str
        """
        self._driver_link = driver_link

    @property
    def code(self):
        """
        Gets the code of this EvaluationRequest.
        base64 encoded code string from user

        :return: The code of this EvaluationRequest.
        :rtype: ByteArray
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this EvaluationRequest.
        base64 encoded code string from user

        :param code: The code of this EvaluationRequest.
        :type code: ByteArray
        """
        self._code = code
