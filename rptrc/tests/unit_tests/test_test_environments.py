"""
Unit tests for test_environment.py.
"""
import os
from pathlib import Path
from unittest import mock
import pytest

from rptrc.src.operators.test_environments import TestEnvironments
from rptrc.src.operators.artifact_properties import ArtifactProperties

VALID_SAMPLE_TEST_ENVIRONMENT = {
    "id": "876asd9fh",
    "requestId": "9876asrb12",
    "name": "theFunOne",
    "status": "Available",
    "pool": "theFunPool",
    "stage": "start",
    "action": "UG",
    "properties": "",
    "additionalInfo": "",
}

VALID_TEST_ENVIRONMENT_PATCH_RESPONSE = {
    'id': 'ckqgt9xbp00020liqcto91bmy',
    'name': 'env1',
    'status': 'Reserved',
    'requestId': 'ckqjjq79i00000ik3bklnfl1h',
    'pools': ['default'],
    'properties': {
        'category': 'Idun1',
        'version': '1.0.0',
        'ccdVersion': '1.0.0',
        'template': 'Temp1',
        'kubeDashboard': 'Kube1',
        'telemetryDashboard': 'Tele1'
    },
    'stage': 'new stage',
    'additionalInfo': 'Reserved by Spinnaker',
    'createdOn': 'Mon, 28 Jun 2021 16:04:13 GMT',
    'modifiedOn': 'Wed, 30 Jun 2021 15:59:25 GMT'
}

SAMPLE_TEST_ENVIRONMENT_1 = {
    'id': 'ltg78dv4673pj378cb',
    'status': 'Reserved',
    'properties': {
        'version': '1.3.2'
    }
}

SAMPLE_TEST_ENVIRONMENT_2 = {
    'id': 'rd674nc67kne34vw',
    'status': 'Standby',
    'properties': {
        'version': '2.8.6'
    }
}

SAMPLE_TEST_ENVIRONMENT_3 = {
    'id': 'ql67ybd45gh4763t',
    'status': 'Reserved',
    'properties': {
        'version': '1.9.7'
    }
}


# pylint: disable=too-many-public-methods
class TestTestEnvironment:
    """
    Class to run unit tests for test_environments.py.
    """

    def test_unreserve_test_environment(self, monkeypatch):
        """
        Tests that we can unreserve a test environment.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='theFunOne')
        monkeypatch.setattr(test_environment, "patch",
                            lambda url, test_environment_body: VALID_SAMPLE_TEST_ENVIRONMENT)
        actual_test_environment = \
            test_environment.unreserve_test_environment()
        assert actual_test_environment == VALID_SAMPLE_TEST_ENVIRONMENT

    def test_unreserve_test_environment_no_patched_test_environment_found(self, monkeypatch):
        """
        Tests that when we unreserve a test environment and no patched test environment is found.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='theFunOne')
        monkeypatch.setattr(test_environment, "patch",
                            lambda url, test_environment_body: {'error'})
        with pytest.raises(Exception) as exception:
            test_environment.unreserve_test_environment()
        expected_exception_value = \
            'Error found in the request response. ' \
            'Failed to unreserve Test Environment!'
        assert str(exception.value) == expected_exception_value

    def test_quarantine_test_environment(self, monkeypatch):
        """
        Tests that we can quarantine a test environment.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='theFunOne')
        monkeypatch.setattr(test_environment, "patch",
                            lambda url, test_environment_body: VALID_SAMPLE_TEST_ENVIRONMENT)
        actual_test_environment = \
            test_environment.quarantine_test_environment()
        assert actual_test_environment == VALID_SAMPLE_TEST_ENVIRONMENT

    def test_quarantine_test_environment_no_patched_test_environment_found(self, monkeypatch):
        """
        Tests that when we quarantine a test environment and no patched test environment is found.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='theFunOne')
        monkeypatch.setattr(test_environment, "patch",
                            lambda url, test_environment_body: {'error'})
        with pytest.raises(Exception) as exception:
            test_environment.quarantine_test_environment()
        expected_exception_value = \
            'Error found in the request response. ' \
            'Failed to quarantine Test Environment!'
        assert str(exception.value) == expected_exception_value

    def test_set_test_environment_to_available(self, monkeypatch):
        """
        Tests that we can set a test environment to available.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='theFunOne')
        monkeypatch.setattr(test_environment, "patch",
                            lambda url, test_environment_body: VALID_SAMPLE_TEST_ENVIRONMENT)
        actual_test_environment = \
            test_environment.set_standby_test_environment_to_available()
        assert actual_test_environment == VALID_SAMPLE_TEST_ENVIRONMENT

    def test_set_test_environment_to_available_no_patched_test_environment_found(self, monkeypatch):
        """
        Tests that when we set a test environment to available and no patched test environment is found.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='theFunOne')
        monkeypatch.setattr(test_environment, "patch",
                            lambda url, test_environment_body: {'error'})
        with pytest.raises(Exception) as exception:
            test_environment.set_standby_test_environment_to_available()
        expected_exception_value = \
            'Error found in the request response. ' \
            'Failed to available Test Environment!'
        assert str(exception.value) == expected_exception_value

    def test_retrieve_test_environment_by_name_test_environment_doesnt_exist(self, monkeypatch):
        """
        Tests the retrieve_test_environment_by_name function when no id is passed and the
        test environment doesn't exist in RPT.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='env2')
        monkeypatch.setattr(test_environment, "get",
                            lambda url: [])
        with pytest.raises(Exception) as exception:
            test_environment.retrieve_test_environment_by_name()
        expected_exception_value = \
            'Test environment "env2" does not exist!'
        assert str(exception.value) == expected_exception_value

    def test_retrieve_test_environment_by_name_duplicate_test_environment_exists(self, monkeypatch):
        """
        Tests the retrieve_test_environment_by_name function when no id is passed and the
        test environment has at least one duplicate (Multiple TEs with same name).
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='env3')
        monkeypatch.setattr(test_environment, "get",
                            lambda url: [{'id': '12345'}, {'id': '12345'}])
        with pytest.raises(Exception) as exception:
            test_environment.retrieve_test_environment_by_name()
        expected_exception_value = \
            'More than one Test Environment exists with the name "env3"!'
        assert str(exception.value) == expected_exception_value

    def test_retrieve_test_environment_by_id_test_environment_doesnt_exist(self, monkeypatch):
        """
        Tests the retrieve_test_environment_by_id function when the
        test environment doesn't exist in RPT.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_id='adg754ji0zsh6')
        monkeypatch.setattr(test_environment, "get",
                            lambda url: [])
        with pytest.raises(Exception) as exception:
            test_environment.retrieve_test_environment_by_id()
        expected_exception_value = \
            'Test environment with id "adg754ji0zsh6" does not exist!'
        assert str(exception.value) == expected_exception_value

    def test_update_test_environment_stage_no_id_passed_test_environment_exists(self, monkeypatch):
        """
        Tests the update_test_environment_stage function when no id is passed and the
        test environment exists in RPT.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='env1')
        monkeypatch.setattr(test_environment, "get",
                            lambda url: [{'id': 'ckqgt9xbp00020liqcto91bmy'}])
        monkeypatch.setattr(test_environment, "patch",
                            lambda url, request_body: VALID_TEST_ENVIRONMENT_PATCH_RESPONSE)
        response = test_environment.update_test_environment_stage('new stage')
        assert response == VALID_TEST_ENVIRONMENT_PATCH_RESPONSE

    def test_update_test_environment_stage_id_passed(self, monkeypatch):
        """
        Tests the update_test_environment_stage function when an id is passed.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name=None)
        monkeypatch.setattr(test_environment, "patch",
                            lambda url, request_body: VALID_TEST_ENVIRONMENT_PATCH_RESPONSE)
        response = test_environment.update_test_environment_stage('new stage',
                                                                  'ckqgt9xbp00020liqcto91bmy')
        assert response == VALID_TEST_ENVIRONMENT_PATCH_RESPONSE

    def test_update_test_environment_stage_error_in_response(self, monkeypatch):
        """
        Tests the update_test_environment_stage function when there's an error
        in the response.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='env1')
        monkeypatch.setattr(test_environment, "patch",
                            lambda url, test_environment_body: {'error'})
        with pytest.raises(Exception) as exception:
            test_environment.update_test_environment_stage('new stage',
                                                           '12345')
        expected_exception_value = \
            'Error found in the request response. ' \
            'Failed to update Test Environment stage!'
        assert str(exception.value) == expected_exception_value

    def test_generate_artifact_properties_has_name_and_folder_exists(self, monkeypatch, tmp_path):
        """
        Tests the generate_artifact_properties function when the test environment
        has a name set and the out folder exists.
        :param monkeypatch:
        """
        monkeypatch.setattr(os.path, "exists", lambda path: True)
        out_dir = tmp_path / 'test/directory'
        out_dir.mkdir(parents=True)

        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='env1')
        artifact_properties = ArtifactProperties({'RESOURCE_NAME': test_environment.test_environment_name},
                                                 out_directory=str(out_dir),
                                                 out_file='artifact.properties')
        artifact_properties.generate()

        file_location = out_dir / artifact_properties.out_file
        actual_file_contents = file_location.read_text()
        expected_file_contents = f'RESOURCE_NAME={test_environment.test_environment_name}\n'
        assert actual_file_contents == expected_file_contents

    def test_generate_artifact_properties_has_name_and_folder_does_not_exist(self, monkeypatch, tmp_path):
        """
        Tests the generate_artifact_properties function when the test environment
        has a name set and the out folder doesn't exist.
        :param monkeypatch:
        """
        def mock_makedirs(path):
            """
            Mock function for os.makedirs.
            :param path:
            """
            directory = Path(path)
            directory.mkdir(parents=True)

        monkeypatch.setattr(os.path, "exists", lambda path: False)
        monkeypatch.setattr(os, "makedirs", mock_makedirs)
        out_dir = tmp_path / 'test/directory'

        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='env1')
        artifact_properties = ArtifactProperties({'RESOURCE_NAME': test_environment.test_environment_name},
                                                 out_directory=str(out_dir),
                                                 out_file='artifact.properties')
        artifact_properties.generate()

        file_location = out_dir / artifact_properties.out_file
        actual_file_contents = file_location.read_text()
        expected_file_contents = f'RESOURCE_NAME={test_environment.test_environment_name}\n'
        assert actual_file_contents == expected_file_contents

    def test_successfully_retrieve_freshest_test_environment(self, monkeypatch):
        """
        Tests retrieve_freshest_test_environment function successful case.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200)
        monkeypatch.setattr(test_environment, "get",
                            lambda url: [SAMPLE_TEST_ENVIRONMENT_2])

        expected_value = [{
            'id': 'rd674nc67kne34vw',
            'status': 'Standby',
            'properties': {
                'version': '2.8.6'
            }
        }]
        assert test_environment\
            .retrieve_freshest_test_environment('ltg78dv4673pj378cb,rd674nc67kne34vw') == expected_value

    def test_retrieve_freshest_test_environment_id_doesnt_exist(self, monkeypatch):
        """
        Tests the retrieve_freshest_test_environment function when test environment
        id passed to the function does not exist.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200)

        monkeypatch.setattr(test_environment, "get",
                            lambda url: [])
        with pytest.raises(Exception) as exception:
            test_environment.retrieve_freshest_test_environment('env1Id,env2Id,env3Id')
        expected_exception_value = \
            'No test environments with ids "env1Id,env2Id,env3Id" found!'
        assert str(exception.value) == expected_exception_value

    def test_retrieve_freshest_test_environment_no_id_passed(self, monkeypatch):
        """
        Tests the retrieve_freshest_test_environment function when no test environment
        id is passed to the function.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200)

        monkeypatch.setattr(test_environment, "get",
                            lambda url: [])
        with pytest.raises(Exception) as exception:
            test_environment.retrieve_freshest_test_environment('')
        expected_exception_value = \
            'No test environments with ids "" found!'
        assert str(exception.value) == expected_exception_value

    def test_retrieve_standby_test_environments(self, monkeypatch):
        """
        Tests the retrieve_standby_test_environments function successful case.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200)

        return_data = [SAMPLE_TEST_ENVIRONMENT_1, SAMPLE_TEST_ENVIRONMENT_2, SAMPLE_TEST_ENVIRONMENT_3]
        test_mock = mock.Mock(side_effect=return_data)
        monkeypatch.setattr(test_environment, "retrieve_test_environment_by_id", test_mock)

        expected_value = ['rd674nc67kne34vw']
        assert test_environment.retrieve_standby_test_environments(['ltg78dv4673pj378cb',
                                                                    'rd674nc67kne34vw',
                                                                    'ql67ybd45gh4763t']) == expected_value

    def test_retrieve_standby_test_environments_no_standby_environment(self, monkeypatch):
        """
        Tests the retrieve_standby_test_environments function where no
        test environments have status "Standby".
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200)

        return_data = [SAMPLE_TEST_ENVIRONMENT_1, SAMPLE_TEST_ENVIRONMENT_3]
        test_mock = mock.Mock(side_effect=return_data)
        monkeypatch.setattr(test_environment, "retrieve_test_environment_by_id", test_mock)

        with pytest.raises(Exception) as exception:
            test_environment.retrieve_standby_test_environments(['ltg78dv4673pj378cb',
                                                                 'ql67ybd45gh4763t'])
        expected_exception_value = \
            'There are no test environments with status "Standby"!'
        assert str(exception.value) == expected_exception_value

    def test_update_test_environment_pool_no_id_passed_test_environment_valid(self, monkeypatch):
        """
        Tests the update_test_environment_pool function when no id is present in the TestEnvironments
        object but the test environment does exist in RPT.
        @param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='env1')
        monkeypatch.setattr(test_environment, "get",
                            lambda url: [{'id': 'ckqgt9xbp00020liqcto91bmd'}])
        monkeypatch.setattr(test_environment, "patch",
                            lambda url, request_body: VALID_TEST_ENVIRONMENT_PATCH_RESPONSE)
        response = test_environment.update_test_environment_pool('new pool')
        assert response == VALID_TEST_ENVIRONMENT_PATCH_RESPONSE

    def test_update_test_environment_pool_id_passed(self, monkeypatch):
        """
        Tests the update_test_environment_pool function when an id is passed.
        :param monkeypatch
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name=None)
        monkeypatch.setattr(test_environment, "patch",
                            lambda url, request_body: VALID_TEST_ENVIRONMENT_PATCH_RESPONSE)
        response = test_environment.update_test_environment_pool('new pool',
                                                                 'ckqgt9xbp00020liqcto91bmd')
        assert response == VALID_TEST_ENVIRONMENT_PATCH_RESPONSE

    def test_update_test_environment_pool_error_in_response(self, monkeypatch):
        """
        Tests the update_test_environment_pool function when there is an error
        in the response.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200, test_environment_name='env1')
        monkeypatch.setattr(test_environment, "patch",
                            lambda url, test_environment_body: {'error'})
        with pytest.raises(Exception) as exception:
            test_environment.update_test_environment_pool('new pool',
                                                          '12345')

        expected_exception_value = \
            'Error found in the request response. Failed to update Test Environment Pools!'
        assert str(exception.value) == expected_exception_value

    def test_check_if_test_environment_on_specified_version_positive_result(self, monkeypatch):
        """
        Tests the check_if_test_environment_on_specified_version function when the version
        on the test environment equals the version specified.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200)
        monkeypatch.setattr(test_environment, "get",
                            lambda url: [{'properties': {'version': '2.35.168'}}])

        result = test_environment.check_if_test_environment_on_specified_version('2.35.168')
        assert result == "true"

    def test_check_if_test_environment_on_specified_version_negative_result(self, monkeypatch):
        """
        Tests the check_if_test_environment_on_specified_version function when the version
        on the test environment does NOT equal the version specified.
        :param monkeypatch:
        """
        test_environment = TestEnvironments(dev_mode=True, retry_timeout=7200)
        monkeypatch.setattr(test_environment, "get",
                            lambda url: [{'properties': {'version': '1.9.27'}}])

        result = test_environment.check_if_test_environment_on_specified_version('2.35.168')
        assert result == "false"
