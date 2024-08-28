"""
Unit tests for pools.py.
"""
import pytest

from rptrc.src.operators.pools import Pools

VALID_SAMPLE_POOL_RESPONSE = {
    "id": "876asd9fh",
    "assignedTestEnvironmentIds": ["9876asrb12"],
    "poolName": "testPool"
}


class TestPool:
    """
    Class to run unit tests for pools.py.
    """

    def test_successfully_retrieve_test_environments_by_pool(self, monkeypatch):
        """
        Tests retrieve_test_environments_by pool function successful case.
        :param monkeypatch:
        """
        pool = Pools(dev_mode=True, retry_timeout=7200, pool_name='testPool')
        monkeypatch.setattr(pool, "get",
                            lambda url: [VALID_SAMPLE_POOL_RESPONSE])

        expected_value = ['9876asrb12']
        assert pool.retrieve_test_environments_by_pool('testPool') == expected_value

    def test_retrieve_test_environments_by_pool_which_doesnt_exist(self, monkeypatch):
        """
        Tests retrieve_test_environments_by pool function where pool
        does not exist.
        :param monkeypatch:
        """
        pool = Pools(dev_mode=True, retry_timeout=7200, pool_name='testPool')
        monkeypatch.setattr(pool, "get",
                            lambda url: [])
        with pytest.raises(Exception) as exception:
            pool.retrieve_test_environments_by_pool('testPool')
        expected_exception_value = \
            'Pool "testPool" does not exist!'
        assert str(exception.value) == expected_exception_value

    def test_retrieve_test_environments_by_pool_no_environments_assigned(self, monkeypatch):
        """
        Tests retrieve_test_environments_by pool function where no
        test environments are assigned to the pool.
        :param monkeypatch:
        """
        pool = Pools(dev_mode=True, retry_timeout=7200, pool_name='testPool')
        monkeypatch.setattr(pool, "get",
                            lambda url: [{"assignedTestEnvironmentIds": []}])
        with pytest.raises(Exception) as exception:
            pool.retrieve_test_environments_by_pool('testPool')
        expected_exception_value = \
            'There are no test environments assigned to pool "testPool"!'
        assert str(exception.value) == expected_exception_value

    def test_update_list_of_pools_pool_to_remove_not_in_list(self):
        """
        Tests that the update_list_of_pools function throws the appropriate error if
        the pool you try to remove, is not currently in the list of pools.
        """
        invalid_pool = 'not_in_pool'
        pool = Pools(dev_mode=True, retry_timeout=7200, pool_name='testPool')
        with pytest.raises(Exception) as exception:
            pool.update_list_of_pools(['a', 'b', 'c'], invalid_pool, 'd')

        expected_exception_value = \
            f'Unable to remove {invalid_pool} from list_of_pools ' \
            'as it is not currently in the list.'
        assert str(exception.value) == expected_exception_value

    def test_update_list_of_pools_pool_to_add_already_in_list(self):
        """
        Tests that the update_list_of_pools function throws the appropriate error if
        the pool you try to add, is already in the list of pools.
        """
        pool_that_already_exists = 'i_already_exist_in_pool'
        pool = Pools(dev_mode=True, retry_timeout=7200, pool_name='testPool')
        with pytest.raises(Exception) as exception:
            pool.update_list_of_pools([pool_that_already_exists, 'b', 'c'],
                                      'b', pool_that_already_exists)

        expected_exception_value = \
            f'Unable to add {pool_that_already_exists} to list_of_pools ' \
            'as it is already in the list.'
        assert str(exception.value) == expected_exception_value

    def test_update_list_of_pools_successfully(self):
        """
        Tests that the update_list_of_pools function conforms to the expected functionality.
        """
        pool = Pools(dev_mode=True, retry_timeout=7200, pool_name='testPool')
        updated_list_of_pools = pool.update_list_of_pools(['a', 'b', 'c'], 'a', 'd')
        assert updated_list_of_pools == ['b', 'c', 'd']
