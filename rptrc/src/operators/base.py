"""
Base module declares common functionality and attributes across Operators
All operators should inherit the base class
"""
import logging

from rptrc.src.etc.exceptions import FatalException


# pylint: disable=too-few-public-methods
class Base:
    """
    The Base class of all operators
    """
    @staticmethod
    def raise_exception_if_error_in_response(response, error_message):
        """
        Raises an exception if there is an error in an object passed
        to this function. Can add a custom error message.
        :param: response
        :param: error_message
        """
        if 'error' in response:
            exception_message = f'Error found in the request response. {error_message}'
            logging.critical(exception_message)
            raise FatalException(exception_message)
