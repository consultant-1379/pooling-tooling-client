"""
CRUD module declares common CRUD functionality and attributes for Operators
They should inherit this class if they are making CRUD operations
"""
import json
import logging
from json import JSONDecodeError

from rptrc.src import configuration
from rptrc.src.etc.exceptions import FatalException
from rptrc.src.etc.request_retry import request_retry


class Crud:
    """
    The CRUD class for operators
    """
    def __init__(self, dev_mode, retry_timeout=7200, proxy=None):
        self.constants = configuration.ApplicationConfig()
        self.target_host = self.__determine_target_host__(dev_mode)
        self.__request_proxy = proxy
        self.__retry_timeout = retry_timeout

    def __determine_target_host__(self, dev_mode):
        """
        Determines the target host based on whether or not we are running in dev mode
        :param dev_mode:
        :return: target_host
        :rtype: str
        """
        if not dev_mode:
            return self.constants.get('RPT_URLS', 'prod')
        logging.debug('Running in dev mode and therefore pointing to staging')
        return self.constants.get('RPT_URLS', 'stag')

    @staticmethod
    def __convert_response_to_json__(response):
        """
        Converts the response to JSON and catches any possible failures
        :param response:
        :return: json_response
        :rtype: dict
        """
        try:
            logging.debug('Attempting to convert response to JSON')
            json_response = response.json()
        except JSONDecodeError as json_error:
            logging.error('Response content:')
            logging.error(str(response.text))
            exception_message = 'Got invalid response from request and could not convert it to JSON!'
            logging.critical(exception_message)
            raise FatalException(exception_message) from json_error
        return json_response

    @staticmethod
    def __convert_request_body_string_to_dict__(request_body):
        """
        Converts the specified Request Body is valid JSON and validating it ss valid JSON in the
        process, raising an exception if its not
        :param request_body:
        :return: request_dict
        :rtype: dict
        """
        try:
            logging.debug('Validating Request Body')
            logging.debug('Request body valid!')
            return json.loads(request_body)
        except ValueError as json_not_valid:
            exception_message = 'When making request, an invalid request body was provided'
            logging.critical(exception_message)
            raise FatalException(exception_message) \
                from json_not_valid

    def get(self, target_url):
        """
        Orchestrates a GET request against the specified target URL
        :param target_url:
        :return: response body
        :rtype: dict
        """
        logging.info(f'Running GET request towards: {target_url}')
        response = request_retry(type_of_request='GET', url=target_url,
                                 retry_timeout=self.__retry_timeout, proxy=self.__request_proxy)
        return self.__convert_response_to_json__(response)

    def put(self, target_url, request_body):
        """
        Orchestrates a PUT request against the specified target URL.
        :param target_url:
        :param request_body:
        :return: response body
        :rtype: dict
        """
        logging.info(f'Running PUT request towards: {target_url}')
        request_body = self.__convert_request_body_string_to_dict__(request_body)
        response = request_retry(type_of_request='PUT', url=target_url, body=request_body,
                                 retry_timeout=self.__retry_timeout, proxy=self.__request_proxy)
        return self.__convert_response_to_json__(response)

    def patch(self, target_url, request_body):
        """
        Orchestrates a PATCH request against the specified target URL.
        :param target_url:
        :param request_body:
        :return: response body
        :rtype: dict
        """
        logging.info(f'Running PATCH request towards: {target_url}')
        request_body = self.__convert_request_body_string_to_dict__(request_body)
        response = request_retry(type_of_request='PATCH', url=target_url, body=request_body,
                                 retry_timeout=self.__retry_timeout, proxy=self.__request_proxy)
        return self.__convert_response_to_json__(response)

    def post(self, target_url, request_body):
        """
        Orchestrates a POST request against the specified target URL.
        :param target_url:
        :param request_body:
        :return: response body
        :rtype: dict
        """
        logging.info(f'Running POST request towards: {target_url}')
        request_body = self.__convert_request_body_string_to_dict__(request_body)
        response = request_retry(type_of_request='POST', url=target_url, body=request_body,
                                 retry_timeout=self.__retry_timeout, proxy=self.__request_proxy)
        return self.__convert_response_to_json__(response)

    def delete(self, target_url):
        """
        Orchestrates a DELETE request against the specified target URL.
        :param target_url:
        """
        logging.info(f'Running DELETE request towards: {target_url}')
        request_retry(type_of_request='DELETE', url=target_url,
                      retry_timeout=self.__retry_timeout, proxy=self.__request_proxy)
