"""
The operator for the Requests RPT service
"""
import json
import logging
import time

from rptrc.src.etc.exceptions import FatalException
from rptrc.src.operators.base import Base
from rptrc.src.operators.crud import Crud


class Requests(Base, Crud):
    """
    Class to handle operations against the Requests RPT service
    """
    def __init__(self, dev_mode, retry_timeout):
        Base.__init__(self)
        Crud.__init__(self, dev_mode, retry_timeout)
        self.requests_url = f'{self.target_host}/api/requests'
        self.rpt_functions_url = f'{self.target_host}/api/pipeline-functions'
        self.sleep_duration = 10

    def get_request_with_id(self, request_id):
        """
        Retrieves a Request entity in RPT that has the specified ID
        :param request_id:
        :return: matching_request
        :rtype: dict
        """
        logging.info(f'Retrieving the Request entity with ID: {request_id}')

        get_url = f'{self.requests_url}/{request_id}'
        matching_requests = self.get(get_url)
        if not matching_requests:
            exception_message = f'No Request entity with ID {request_id} was found in RPT'
            logging.critical(exception_message)
            raise FatalException(exception_message)

        matching_request = matching_requests[0]
        logging.debug(f'SUCCESS: Retrieved request matching ID {request_id}')
        logging.debug(str(matching_request))
        return matching_request

    def abort_request_by_id(self, request_id):
        """
        Aborts a Request entity in RPT that has the specified ID
        :param request_id:
        :return: request_response
        :rtype: dict
        """
        logging.info(f'Aborting the Request entity with ID: {request_id}')

        patch_url = f'{self.rpt_functions_url}/request-from-queued-to-aborted/{request_id}'

        response = self.patch(patch_url, '{}')
        logging.debug(f'Response: {str(response)}')

        self.raise_exception_if_error_in_response(response, 'Failed to abort request, please contact Thunderbee.')

        logging.info(f'SUCCESS: Request Aborted - {self.requests_url}/{request_id}')
        return response

    def create_queued_request(self, request_body: dict):
        """
        Creates a new queued Request entity in RPT
        :param request_body:
        :return: request
        :rtype: dict
        """
        logging.info('Creating a new queued Request entity')

        try:
            request_body['requestorDetails']['executionId'] \
                = request_body['requestorDetails']['executionId'].split('/')[8]
        except (KeyError, IndexError) as request_body_modification_exception:
            exception_message = ('Error found in the request body. '
                                 'Failed to create a new queued request!')
            logging.critical(exception_message)
            raise FatalException(exception_message) from request_body_modification_exception

        logging.debug(f'Request Body: {str(request_body)}')

        created_request = self.post(self.requests_url, json.dumps(request_body))

        if 'error' in created_request:
            exception_message = ('Error found in the request response. '
                                 'Failed to create a new queued request!')
            logging.critical(exception_message)
            raise FatalException(exception_message)

        logging.debug(f'Created Request: {str(created_request)}')

        logging.info('SUCCESS: Created a queued Request entity')
        return created_request

    def wait_for_the_queued_request_be_resolved(self, request_id):
        """
        For a queued Request with the specified ID, it will poll RPT until the Request status is
        either set to reserved or timeout
        :param request_id:
        :return: request
        :rtype: dict
        """
        logging.info('Waiting for the queued request to be resolved.')
        request = self.get_request_with_id(request_id)

        while request['status'] == 'Queued':
            logging.info(f'Request still queued. Sleeping for {self.sleep_duration} '
                         f'seconds and will try again.')
            time.sleep(self.sleep_duration)
            request = self.get_request_with_id(request_id)

        request_status = request["status"]
        if request_status == 'Timeout':
            exception_message = ('Request timed out, there are no available environments. '
                                 'Please try again')
            logging.critical(exception_message)
            raise FatalException(exception_message)
        if request_status == 'Aborted':
            exception_message = 'Request aborted.'
            logging.critical(exception_message)
            raise FatalException(exception_message)

        logging.info(f'SUCCESS: Request is now in a "{request_status}" status')
        return request
