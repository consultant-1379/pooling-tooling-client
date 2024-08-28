"""
The operator for the RPT Test Environment RPT service.
"""
import json
import logging

from rptrc.src.etc.exceptions import FatalException
from rptrc.src.operators.base import Base
from rptrc.src.operators.crud import Crud


class TestEnvironments(Base, Crud):
    """
    Class to handle operations against the RPT Test Environments service.
    """
    def __init__(self, dev_mode, retry_timeout, test_environment_name=None, test_environment_id=None):
        Base.__init__(self)
        Crud.__init__(self, dev_mode, retry_timeout)
        self.test_environment_name = test_environment_name
        self.test_environment_id = test_environment_id
        self.test_environment_url = f'{self.target_host}/api/test-environments'
        self.rpt_functions_url = f'{self.target_host}/api/pipeline-functions'

    def retrieve_test_environment_by_name(self):
        """
        Retrieves a test environment from RPT.
        :return: test_environment
        :rtype: dict
        """
        logging.info('Retrieving Test Environment From RPT based on name')

        get_url = f'{self.test_environment_url}/' \
                  f'/name/{self.test_environment_name}'

        response = self.get(get_url)
        logging.debug(f'Response: {str(response)}')

        self.raise_exception_if_error_in_response(response, 'Failed to retrieve test environment.')

        if len(response) < 1:
            exception_message = f'Test environment "{self.test_environment_name}" does not exist!'
            logging.critical(exception_message)
            raise FatalException(exception_message)
        if len(response) > 1:
            exception_message = f'More than one Test Environment exists with the name "{self.test_environment_name}"!'
            logging.critical(exception_message)
            raise FatalException(exception_message)
        return response[0]

    def retrieve_test_environment_by_id(self):
        """
        Retrieves a test environment from RPT based on id.
        :return: test_environment
        :rtype: dict
        """
        logging.info('Retrieving Test Environment From RPT based on id')

        get_url = f'{self.test_environment_url}/' \
                  f'/{self.test_environment_id}'

        response = self.get(get_url)
        logging.debug(f'Response: {str(response)}')

        self.raise_exception_if_error_in_response(response, 'Failed to retrieve test environment.')

        if len(response) < 1:
            exception_message = f'Test environment with id "{self.test_environment_id}" does not exist!'
            logging.critical(exception_message)
            raise FatalException(exception_message)
        return response[0]

    def unreserve_test_environment(self):
        """
        Unreserves a test environment in RPT.
        :return: response
        :rtype: dict
        """
        logging.info('Unreserving a Test Environment')

        patch_url = f'{self.rpt_functions_url}/' \
                    f'test-environment-from-reserved-to-available/{self.test_environment_name}'

        response = self.patch(patch_url, '{}')
        logging.debug(f'Response: {str(response)}')

        self.raise_exception_if_error_in_response(response, 'Failed to unreserve Test Environment!')

        logging.info('SUCCESS: Unreserved Test Environment')
        return response

    def quarantine_test_environment(self):
        """
        Quarantines a test environment in RPT.
        :return: response
        :rtype: dict
        """
        logging.info('Quarantining a Test Environment')

        patch_url = f'{self.rpt_functions_url}/' \
                    f'test-environment-from-reserved-to-quarantined/{self.test_environment_name}'

        response = self.patch(patch_url, '{}')
        logging.debug(f'Response: {str(response)}')

        self.raise_exception_if_error_in_response(response, 'Failed to quarantine Test Environment!')

        logging.info('SUCCESS: Quarantined Test Environment')
        return response

    def set_standby_test_environment_to_available(self):
        """
        Sets a standby test environment to available in RPT.
        :return: response
        :rtype: dict
        """
        logging.info('Setting Test Environment to Available')

        patch_url = f'{self.rpt_functions_url}/' \
                    f'test-environment-from-standby-to-available/{self.test_environment_name}'

        response = self.patch(patch_url, '{}')
        logging.debug(f'Response: {str(response)}')

        self.raise_exception_if_error_in_response(response, 'Failed to available Test Environment!')

        logging.info('SUCCESS: Set Test Environment to Available')
        return response

    def update_test_environment_stage(self, pipeline_stage, test_environment_id=None):
        """
        Updates a test environment's stage in RPT.
        :param: pipeline_stage
        :param: test_environment_id
        :return: response
        :rtype: dict
        """
        if test_environment_id is None:
            test_environment_id = self.retrieve_test_environment_by_name()["id"]

        logging.info('Updating Test Environment Stage')

        patch_url = f'{self.test_environment_url}/' \
                    f'{test_environment_id}'

        request_body = {}
        request_body['stage'] = pipeline_stage

        response = self.patch(patch_url, json.dumps(request_body))
        logging.debug(f'Response: {str(response)}')

        self.raise_exception_if_error_in_response(response, 'Failed to update Test Environment stage!')

        logging.info('SUCCESS: Updated Test Environment Stage')
        return response

    def retrieve_standby_test_environments(self, test_environment_ids):
        """
        Retrieves test environments with status 'Standby' from a list of test
        environment ids.
        :param: test_environment_ids
        :return: standby_test_environments
        :rtype: list
        """
        logging.info('Retrieving Standby test environments')

        standby_test_environments = []
        for test_environment_id in test_environment_ids:
            self.test_environment_id = test_environment_id
            retrieved_test_environment = self.retrieve_test_environment_by_id()
            if retrieved_test_environment["status"] == 'Standby':
                standby_test_environments.append(test_environment_id)

        if len(standby_test_environments) < 1:
            exception_message = 'There are no test environments with status "Standby"!'
            logging.critical(exception_message)
            raise FatalException(exception_message)

        return standby_test_environments

    def retrieve_freshest_test_environment(self, test_environment_ids):
        """
        Retrieves the freshest test environment from RPT based on version.
        :param: test_environment_ids
        :return: response
        :rtype: dict
        """
        logging.info('Retrieving freshest test environment')

        get_url = f'{self.test_environment_url}/' \
                  f'/get-freshest-test-environment/{test_environment_ids}'

        response = self.get(get_url)
        logging.debug(f'Response: {str(response)}')

        self.raise_exception_if_error_in_response(response, 'Failed to retrieve test environment.')

        if len(response) < 1:
            exception_message = f'No test environments with ids "{test_environment_ids}" found!'
            logging.critical(exception_message)
            raise FatalException(exception_message)

        return response

    def update_test_environment_pool(self, new_list_of_pools, test_environment_id=None):
        """
        Updates a test environment's pool in RPT.
        :param: new_list_of_pools
        :param: test_environment_id
        :return: response
        :rtype: dict
        """

        if test_environment_id is None:
            test_environment_id = self.retrieve_test_environment_by_name()["id"]

        logging.info('Updating Test Environment Pool')

        patch_url = f'{self.test_environment_url}/' \
                    f'{test_environment_id}'

        request_body = {}
        request_body['pools'] = new_list_of_pools

        response = self.patch(patch_url, json.dumps(request_body))
        logging.debug(f'Response: {str(response)}')

        self.raise_exception_if_error_in_response(response, 'Failed to update Test Environment Pools!')

        logging.info('SUCCESS: Updated Test Environment Pools')
        return response

    def check_if_test_environment_on_specified_version(self, version_for_comparison):
        """
        Checks if EIC version on a test environment equals that specified.
        :param: version_for_comparison
        :return: result
        :rtype: str
        """
        test_environment_to_check = self.retrieve_test_environment_by_name()
        result = "false"
        if test_environment_to_check['properties']['version'] == version_for_comparison:
            result = "true"
        return result
