"""
The operator for the RPT Pool RPT service.
"""
import logging

from rptrc.src.etc.exceptions import FatalException
from rptrc.src.operators.base import Base
from rptrc.src.operators.crud import Crud


class Pools(Base, Crud):
    """
    Class to handle operations against the RPT Pools service.
    """
    def __init__(self, dev_mode, retry_timeout, pool_name):
        Base.__init__(self)
        Crud.__init__(self, dev_mode, retry_timeout)
        self.pool_name = pool_name
        self.pool_url = f'{self.target_host}/api/pools'
        self.rpt_functions_url = f'{self.target_host}/api/pipeline-functions'

    def retrieve_test_environments_by_pool(self, pool_name):
        """
        Retrieves all test environments in specified pool from RPT.
        :param: pool_name
        :return: test_environments
        :rtype: list
        """
        logging.info('Retrieving Test Environment Ids for Specified Pool From RPT')

        get_url = f'{self.pool_url}/' \
                  f'/name/{pool_name}'

        response = self.get(get_url)
        logging.debug(f'Response: {str(response)}')

        self.raise_exception_if_error_in_response(response, 'Failed to retrieve test environments.')

        if len(response) < 1:
            exception_message = f'Pool "{self.pool_name}" does not exist!'
            logging.critical(exception_message)
            raise FatalException(exception_message)

        test_environments_in_pool = response[0]["assignedTestEnvironmentIds"]

        if len(test_environments_in_pool) < 1:
            exception_message = f'There are no test environments assigned to pool "{pool_name}"!'
            logging.critical(exception_message)
            raise FatalException(exception_message)

        return test_environments_in_pool

    @staticmethod
    def update_list_of_pools(list_of_pools, pool_to_remove, pool_to_add):
        """
        Takes in a list of pools, the pool to remove from the list and pool to add to the list,
        and will return the reformatted list of pools
        :param: list_of_pools
        :param: pool_to_remove
        :param: pool_to_add
        :return: list_of_pools
        :rtype: list
        """

        if pool_to_remove not in list_of_pools:
            exception_message = (f'Unable to remove {pool_to_remove} from list_of_pools as it '
                                 'is not currently in the list.')
            logging.critical(exception_message)
            raise FatalException(exception_message)
        if pool_to_add in list_of_pools:
            exception_message = (f'Unable to add {pool_to_add} to list_of_pools as it is '
                                 'already in the list.')
            logging.critical(exception_message)
            raise FatalException(exception_message)

        list_of_pools.remove(pool_to_remove)
        list_of_pools.append(pool_to_add)
        return list_of_pools
