"""
Unit tests for crud.py
"""
import pytest

from rptrc.src import configuration
from rptrc.src.operators.crud import Crud
from rptrc.tests.unit_tests.mock_response import MockResponse

CONSTANTS = configuration.ApplicationConfig()

VALID_JSON_STRING = '''{
    "key": "value"
}'''

VALID_JSON_DICT = {
    "key": "value"
}

INVALID_JSON_STRING = '''{
    "key": "value"
    "another": "one"
}'''


class TestCrud:
    """
    Class to run unit tests for crud.py
    """

    def test_determine_target_host_prod(self):
        """
        Test that if we are running in production mode, we return the production URL
        """
        dev_mode = False
        crud_prod_mode = Crud(dev_mode=dev_mode)
        actual_target_host = crud_prod_mode.__determine_target_host__(dev_mode)
        expected_target_host = CONSTANTS.get('RPT_URLS', 'prod')
        assert actual_target_host == expected_target_host

    def test_determine_target_host_dev(self):
        """
        Test that if we are running in development mode, we return the staging URL
        """
        dev_mode = True
        crud_dev_mode = Crud(dev_mode=dev_mode)
        actual_target_host = crud_dev_mode.__determine_target_host__(dev_mode)
        expected_target_host = CONSTANTS.get('RPT_URLS', 'stag')
        assert actual_target_host == expected_target_host

    def test_convert_response_to_json(self):
        """
        Test that we can convert a response to JSON successfully
        """
        crud = Crud(dev_mode=True)
        mock_response = MockResponse(VALID_JSON_STRING, 200)
        actual_response = crud.__convert_response_to_json__(mock_response)
        expected_response = {
            "key": "value"
        }
        assert actual_response == expected_response

    def test_convert_response_to_json_invalid(self):
        """
        Test that we handle the scenario where we get an invalid response from a request
        """
        crud = Crud(dev_mode=True)
        mock_response = MockResponse(INVALID_JSON_STRING, 200)
        with pytest.raises(Exception) as exception:
            crud.__convert_response_to_json__(mock_response)
        expected_exception_value = \
            'Got invalid response from request and could not convert it to JSON!'
        assert str(exception.value) == expected_exception_value

    def test_validate_request_body(self):
        """
        Test that we can check if a valid request body is valid JSON
        """
        crud = Crud(dev_mode=True)
        actual_response = crud.__convert_request_body_string_to_dict__(VALID_JSON_STRING)
        assert actual_response == VALID_JSON_DICT

    def test_validate_request_body_invalid(self):
        """
        Test that we catch an invalid request body that isn't JSON
        """
        crud = Crud(dev_mode=True)
        with pytest.raises(Exception) as exception:
            crud.__convert_request_body_string_to_dict__(INVALID_JSON_STRING)
        expected_exception_value = \
            'When making request, an invalid request body was provided'
        assert str(exception.value) == expected_exception_value
