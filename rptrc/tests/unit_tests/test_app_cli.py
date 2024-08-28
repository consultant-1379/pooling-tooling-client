"""
Unit tests for app_cli.py
"""
from unittest import mock

from click.testing import CliRunner
from rptrc.src.app_cli import (
    create_queued_request,
    abort_queued_request,
    store_details_for_test_environments_by_pool,
    unreserve_environment,
    quarantine_environment,
    set_standby_environment_to_available,
    update_test_environment_stage,
    store_test_environment_details,
    retrieve_test_environment_details,
    fail_if_version_specified_equals_version_on_test_environment,
    check_if_version_specified_equals_version_on_test_environment,
    update_freshest_standby_test_environment_to_available,
    swap_in_available_environment_swap_out_current_environment,
    swap_test_environment_pool,
    update_freshest_standby_env_to_available_and_swap_its_pool
)
from rptrc.src.operators.artifact_properties import ArtifactProperties

VALID_ARTIFACT_REQUEST_ID = {
    'REQUEST_ID': 'ckuctyf5j00000ppcdfd16196',
}

VALID_ARTIFCAT_TEST_ENVIRONMENT_ID = {
    'AVAILABLE_TEST_ENVIRONMENT_ID': 'ckuctyf5j00000ppcdfd16196'
}

VALID_ABORT_REQUEST_RESPONSE = '''{
    'id': 'ckuctyf5j00000ppcdfd16196',
    'testEnvironmentId': '',
    'poolName': 'j',
    'requestorDetails': {
        'name': 'jack',
        'area': 'local test'
    },
    'status': 'Aborted',
    'createdOn': 'Mon, 04 Oct 2021 15:51:00 GMT',
    'modifiedOn': 'Mon, 04 Oct 2021 15:51:19 GMT',
    'lastReservedAt': 'Mon, 04 Oct 2021 15:51:19 GMT'
}'''

VALID_REQUEST_BODY = {
    'poolName': 'testPool',
    'requestorDetails': {
        'name': 'Spinnaker',
        'area': 'IDUN',
        'executionId': 'https://spinnaker.rnd.gic.ericsson.se'
                       '/#/applications/product-e2e-cicd/executions'
                       '/details/01FTZPSYFZ7V3XWMME5BA358QT'
    },
    'status': 'Queued'
}

VALID_SAMPLE_POOL_RESPONSE = [{
    'id': 'ckuctyf5j00000ppcdfd16196',
    'assignedTestEnvironmentIds': ['9876asrb12'],
    'poolName': 'testPool'
}]

VALID_SAMPLE_REQUEST = {
    'id': 'ckuctyf5j00000ppcdfd16196',
    'testEnvironmentId': '9876asrb12',
    'poolName': 'theFunOne',
    'requestorDetails': {
        'name': 'John Doe',
        'area': 'Product Staging',
        'executionId': 'https://spinnaker.rnd.gic.ericsson.se'
                       '/#/applications/product-e2e-cicd/executions'
                       '/details/01FTZPSYFZ7V3XWMME5BA358QT'
    },
    'status': 'Queued'
}

VALID_SAMPLE_TEST_ENVIRONMENT = {
    'id': 'ckuctyf5j00000ppcdfd16196',
    'requestId': '9876asrb12',
    'name': 'validTestEnvironment',
    'status': 'Available',
    'pools': ['validPool'],
    'properties': {
        'category': 'Idun1',
        'version': '1.0.0',
        'ccdVersion': '1.0.0',
        'template': 'Temp1',
        'kubeDashboard': 'Kube1',
        'telemetryDashboard': 'Tele1'
    },
    'stage': 'start',
    'action': 'UG',
    'additionalInfo': '',
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

SAMPLE_TEST_ENVIRONMENT = {
    'id': '9876asrb12',
    'name': 'sampleTestEnvironment',
    'status': 'Standby',
    'properties': {
        'version': '2.8.6'
    }
}

SAMPLE_TEST_ENVIRONMENT_SET_TO_AVAILABLE = {
    'id': '9876asrb12',
    'name': 'sampleTestEnvironment',
    'status': 'Available',
    'properties': {
        'version': '2.8.6'
    }
}

SAMPLE_VALID_POOL_WITH_STANDBY_ENV_ATTACHED = {
    'id': 'ckuctyf5j00000ppcdfd16196',
    'assignedTestEnvironmentIds': ['asdfjkl1234'],
    'poolName': 'validPool'
}

SAMPLE_VALID_TEST_ENV_SET_TO_STANDBY = {
    'id': 'asdfjkl1234',
    'requestId': '9876asrb12',
    'name': 'validTestEnvironment',
    'status': 'Standby',
    'pools': ['validPool'],
    'properties': {
        'category': 'Idun1',
        'version': '1.0.0',
        'ccdVersion': '1.0.0',
        'template': 'Temp1',
        'kubeDashboard': 'Kube1',
        'telemetryDashboard': 'Tele1'
    },
    'stage': 'start',
    'action': 'UG',
    'additionalInfo': '',
}


# pylint: disable=too-many-public-methods
# pylint: disable=line-too-long
class TestAppCli:
    """
    Class to run unit tests for test_environments.py.
    """
    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    @mock.patch('rptrc.src.etc.request_retry.requests.post')
    def test_create_queued_request(self, mock_post, mock_get, mock_patch):
        """
        Tests create_queued_request CLI command.
        :param
        :param
        """

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = VALID_SAMPLE_REQUEST
        mock_get.return_value.status_code = 200
        mock_post.return_value.json.return_value = VALID_SAMPLE_REQUEST
        mock_patch.return_value.status_code = 200
        mock_post.return_value.json.return_value = VALID_TEST_ENVIRONMENT_PATCH_RESPONSE

        runner = CliRunner()
        result = runner.invoke(create_queued_request,
                               [
                                "-ps", "new stage",
                                "-b", '''{
                                    "poolName": "validPool",
                                    "requestorDetails": {
                                        "name": "Spinnaker",
                                        "area": "IDUN",
                                        "executionId":
                                        "https://spinnaker-pipeline-url/#/projects/oss_e2e_cicd/applications/eiap-release-e2e-cicd/executions/01G7VS096KJ8FNKEQRMDSXX842"
                                    },
                                    "status": "Queued"
                                    }''',
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    @mock.patch('rptrc.src.etc.request_retry.requests.post')
    def test_create_queued_request_with_error(self, mock_post, mock_get, mock_patch):
        """
        Tests create_queued_request CLI command with error.
        :param
        :param
        """

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = VALID_SAMPLE_REQUEST
        mock_get.return_value.status_code = 400
        mock_post.return_value.json.return_value = {'error'}
        mock_patch.return_value.status_code = 200
        mock_post.return_value.json.return_value = VALID_TEST_ENVIRONMENT_PATCH_RESPONSE

        runner = CliRunner()
        result = runner.invoke(create_queued_request,
                               [
                                "-ps", "new stage",
                                "-b", '''{
                                    "poolName": "validPool",
                                    "requestorDetails": {
                                        "name": "Spinnaker",
                                        "area": "IDUN",
                                        "executionId":
                                        "https://spinnaker-pipeline-url/#/projects/oss_e2e_cicd/applications/eiap-release-e2e-cicd/executions/01G7VS096KJ8FNKEQRMDSXX842"
                                    },
                                    "status": "Queued"
                                    }''',
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch.object(ArtifactProperties, 'read')
    def test_abort_queued_request(self, read, mock_patch):
        """
        Tests abort_queued_request CLI command.
        :param read:
        :param mock_patch:
        """
        read.return_value = VALID_ARTIFACT_REQUEST_ID
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = VALID_ABORT_REQUEST_RESPONSE

        runner = CliRunner()
        result = runner.invoke(abort_queued_request, ["--verbose", "--dev_mode"])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch.object(ArtifactProperties, 'read')
    def test_abort_queued_request_error(self, read, mock_patch):
        """
        Tests abort_queued_request CLI command with error.
        :param read:
        :param mock_patch:
        """
        read.return_value = VALID_ARTIFACT_REQUEST_ID
        mock_patch.return_value.status_code = 400
        mock_patch.return_value.json.return_value = {'error'}

        runner = CliRunner()
        result = runner.invoke(abort_queued_request, ["--verbose", "--dev_mode"])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    def test_unreserve_test_environment(self, mock_patch):
        """
        Tests unreserve_environment CLI command.
        :param mock_patch:
        """
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = VALID_SAMPLE_TEST_ENVIRONMENT

        runner = CliRunner()
        result = runner.invoke(unreserve_environment, ["-t", "validTestEnvironment", "--verbose", "--dev_mode"])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    def test_unreserve_test_environment_error(self, mock_patch):
        """
        Tests unreserve_environment CLI command with error.
        :param mock_patch:
        """
        mock_patch.return_value.status_code = 400
        mock_patch.return_value.json.return_value = {'error'}

        runner = CliRunner()
        result = runner.invoke(unreserve_environment, ["-t", "validTestEnvironment", "--verbose", "--dev_mode"])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    def test_quarantine_environment(self, mock_patch):
        """
        Tests quarantine_environment CLI command.
        :param mock_patch:
        """
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = VALID_SAMPLE_TEST_ENVIRONMENT
        runner = CliRunner()
        result = runner.invoke(quarantine_environment, ["-t", "validTestEnvironment", "--verbose", "--dev_mode"])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    def test_quarantine_environment_error(self, mock_patch):
        """
        Tests quarantine_environment CLI command with error.
        :param mock_patch:
        """
        mock_patch.return_value.status_code = 400
        mock_patch.return_value.json.return_value = {'error'}
        runner = CliRunner()
        result = runner.invoke(quarantine_environment, ["-t", "validTestEnvironment", "--verbose", "--dev_mode"])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    def test_set_standby_environment_to_available(self, mock_patch):
        """
        Tests set_standby_environment_to_available CLI command.
        :param mock_patch:
        """
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = VALID_SAMPLE_TEST_ENVIRONMENT

        runner = CliRunner()
        result = runner.invoke(set_standby_environment_to_available,
                               [
                                "-t", "validTestEnvironment",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    def test_set_standby_environment_to_available_error(self, mock_patch):
        """
        Tests set_standby_environment_to_available CLI command with error.
        :param mock_patch:
        """
        mock_patch.return_value.status_code = 400
        mock_patch.return_value.json.return_value = {'error'}

        runner = CliRunner()
        result = runner.invoke(set_standby_environment_to_available,
                               [
                                "-t", "validTestEnvironment",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_update_test_environment_stage(self, mock_get, mock_patch):
        """
        Tests update_test_environment_stage CLI command.
        :param mock_get:
        :param mock_patch:
        """

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'id': 'ckqgt9xbp00020liqcto91bmy'}]
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = VALID_TEST_ENVIRONMENT_PATCH_RESPONSE

        runner = CliRunner()
        result = runner.invoke(update_test_environment_stage,
                               [
                                "-t", "validTestEnvironment",
                                "-ps", "new stage",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_update_test_environment_stage_error(self, mock_get, mock_patch):
        """
        Tests update_test_environment_stage CLI command with error.
        :param mock_get:
        :param mock_patch:
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'id': 'ckqgt9xbp00020liqcto91bmy'}]
        mock_patch.return_value.status_code = 400
        mock_patch.return_value.json.return_value = {'error'}

        runner = CliRunner()
        result = runner.invoke(update_test_environment_stage,
                               [
                                "-t", "validTestEnvironment",
                                "-ps", "new stage",
                                "--verbose",
                                "--dev_mode"
                                ])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_store_test_environment_details(self, mock_get, mock_patch):
        """
        Tests store_test_environment_details CLI command.
        :param mock_get:
        :param mock_patch:
        """

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'id': 'ckuctyf5j00000ppcdfd16196'}]
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = VALID_SAMPLE_TEST_ENVIRONMENT

        runner = CliRunner()
        result = runner.invoke(store_test_environment_details,
                               [
                                "-t", "validTestEnvironment",
                                "-b", '''{
                                    "poolName": "validPool",
                                    "requestorDetails": {
                                        "name": "Spinnaker",
                                        "area": "IDUN",
                                        "executionId": "https://spinnaker-pipeline-url"
                                    },
                                    "status": "Queued"
                                    }''',
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_store_test_environment_details_error(self, mock_get, mock_patch):
        """
        Tests store_test_environment_details CLI command with error.
        :param mock_get:
        :param mock_patch:
        """

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'id': 'ckuctyf5j00000ppcdfd16196'}]
        mock_patch.return_value.status_code = 400
        mock_patch.return_value.json.return_value = {'error'}

        runner = CliRunner()
        result = runner.invoke(store_test_environment_details,
                               [
                                "-t", "validTestEnvironment",
                                "-b", '''{
                                    "poolName": "validPool",
                                    "requestorDetails": {
                                        "name": "Spinnaker",
                                        "area": "IDUN",
                                        "executionId": "https://spinnaker-pipeline-url"
                                    },
                                    "status": "Queued"
                                    }''',
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_store_details_for_test_environments_by_pool(self, mock_get, mock_patch):
        """
        Tests store_details_for_test_environments_by_pool CLI command.
        :param mock_get:
        :param mock_patch:
        """
        fake_get_responses = [mock.Mock(), mock.Mock()]
        fake_get_responses[0].status_code = 200
        fake_get_responses[0].json.return_value = VALID_SAMPLE_POOL_RESPONSE
        fake_get_responses[1].status_code = 200
        fake_get_responses[1].json.return_value = [{'id': 'ckuctyf5j00000ppcdfd16196'}]
        mock_get.side_effect = fake_get_responses
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = VALID_SAMPLE_TEST_ENVIRONMENT

        runner = CliRunner()
        result = runner.invoke(store_details_for_test_environments_by_pool,
                               [
                                "-pl", "validPool",
                                "-b", '''{
                                    "poolName": "validPool",
                                    "requestorDetails": {
                                        "name": "Spinnaker",
                                        "area": "IDUN",
                                        "executionId":
                                        "https://spinnaker-pipeline-url/#/projects/oss_e2e_cicd/applications/eiap-release-e2e-cicd/executions/01G7VS096KJ8FNKEQRMDSXX842"
                                    },
                                    "status": "Queued"
                                    }''',
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_store_details_for_test_environments_by_pool_error(self, mock_get, mock_patch):
        """
        Tests store_details_for_test_environments_by_pool CLI command with error.
        :param mock_get:
        :param mock_patch:
        """
        fake_get_responses = [mock.Mock(), mock.Mock()]
        fake_get_responses[0].status_code = 200
        fake_get_responses[0].json.return_value = VALID_SAMPLE_POOL_RESPONSE
        fake_get_responses[1].status_code = 200
        fake_get_responses[1].json.return_value = [{'id': 'ckuctyf5j00000ppcdfd16196'}]
        mock_get.side_effect = fake_get_responses
        mock_patch.return_value.status_code = 400
        mock_patch.return_value.json.return_value = {'error'}

        runner = CliRunner()
        result = runner.invoke(store_details_for_test_environments_by_pool,
                               [
                                "-pl", "validPool",
                                "-b", '''{
                                    "poolName": "validPool",
                                    "requestorDetails": {
                                        "name": "Spinnaker",
                                        "area": "IDUN",
                                        "executionId":
                                        "https://spinnaker-pipeline-url/#/projects/oss_e2e_cicd/applications/eiap-release-e2e-cicd/executions/01G7VS096KJ8FNKEQRMDSXX842"
                                    },
                                    "status": "Queued"
                                    }''',
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_retrieve_test_environment_details(self, mock_get):
        """
        Tests retrieve_test_environment_details CLI command.
        :param :
        """

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [SAMPLE_TEST_ENVIRONMENT]

        runner = CliRunner()
        result = runner.invoke(retrieve_test_environment_details,
                               [
                                "-t", "validTestEnvironment",
                                "--verbose",
                                "--dev_mode"
                               ])
        result.exit_code = 0

    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_retrieve_test_environment_details_error(self, mock_get):
        """
        Tests retrieve_test_environment_details CLI command with error.
        :param :
        """

        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = {'error'}

        runner = CliRunner()
        result = runner.invoke(retrieve_test_environment_details,
                               [
                                "-t", "validTestEnvironment",
                                "--verbose",
                                "--dev_mode"
                               ])
        result.exit_code = 0

    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_fail_if_version_specified_equals_version_on_test_environment_with_matching_version(self, mock_get):
        """
        Tests fail_if_version_specified_equals_version_on_test_environment CLI command.
        :param mock_get:
        """

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [SAMPLE_TEST_ENVIRONMENT]

        runner = CliRunner()
        result = runner.invoke(fail_if_version_specified_equals_version_on_test_environment,
                               [
                                "-t", "validTestEnvironment",
                                "-vfc", "2.8.6",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_fail_if_version_specified_equals_version_on_test_environment_without_matching_version(self, mock_get):
        """
        Tests fail_if_version_specified_equals_version_on_test_environment CLI command.
        :param mock_get:
        """

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [SAMPLE_TEST_ENVIRONMENT]

        runner = CliRunner()
        result = runner.invoke(fail_if_version_specified_equals_version_on_test_environment,
                               [
                                "-t", "validTestEnvironment",
                                "-vfc", "1.3.1",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_check_if_version_specified_equals_version_on_test_environment(self, mock_get):
        """
        Tests check_if_version_specified_equals_version_on_test_environment CLI command.
        :param mock_get:
        """

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [SAMPLE_TEST_ENVIRONMENT]

        runner = CliRunner()
        result = runner.invoke(check_if_version_specified_equals_version_on_test_environment,
                               [
                                "-t", "validTestEnvironment",
                                "-vfc", "2.8.6",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_check_if_version_specified_equals_version_on_test_environment_error(self, mock_get):
        """
        Tests check_if_version_specified_equals_version_on_test_environment CLI command with error.
        :param mock_get:
        """

        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = {'error'}

        runner = CliRunner()
        result = runner.invoke(check_if_version_specified_equals_version_on_test_environment,
                               [
                                "-t", "validTestEnvironment",
                                "-vfc", "1.3.1",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_update_freshest_standby_test_environment_to_available(self, mock_get, mock_patch):
        """
        Tests update_freshest_standby_test_environment_to_available CLI command.
        :param mock_get:
        :param mock_patch:
        """

        fake_get_responses = [mock.Mock(), mock.Mock(), mock.Mock()]
        fake_get_responses[0].status_code = 200
        fake_get_responses[0].json.return_value = VALID_SAMPLE_POOL_RESPONSE
        fake_get_responses[1].status_code = 200
        fake_get_responses[1].json.return_value = [SAMPLE_TEST_ENVIRONMENT]
        fake_get_responses[2].status_code = 200
        fake_get_responses[2].json.return_value = SAMPLE_TEST_ENVIRONMENT
        mock_get.side_effect = fake_get_responses
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = SAMPLE_TEST_ENVIRONMENT_SET_TO_AVAILABLE

        runner = CliRunner()
        result = runner.invoke(update_freshest_standby_test_environment_to_available,
                               [
                                "-pl", "validPool",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_update_freshest_standby_test_environment_to_available_error(self, mock_get, mock_patch):
        """
        Tests update_freshest_standby_test_environment_to_available CLI command with error.
        :param mock_get:
        """

        fake_get_responses = [mock.Mock(), mock.Mock(), mock.Mock()]
        fake_get_responses[0].status_code = 200
        fake_get_responses[0].json.return_value = VALID_SAMPLE_POOL_RESPONSE
        fake_get_responses[1].status_code = 200
        fake_get_responses[1].json.return_value = [SAMPLE_TEST_ENVIRONMENT]
        fake_get_responses[2].status_code = 400
        fake_get_responses[2].json.return_value = {'error'}
        mock_get.side_effect = fake_get_responses
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = SAMPLE_TEST_ENVIRONMENT_SET_TO_AVAILABLE

        runner = CliRunner()
        result = runner.invoke(update_freshest_standby_test_environment_to_available,
                               [
                                "-pl", "validPool",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    @mock.patch.object(ArtifactProperties, 'read')
    def test_swap_in_available_environment_swap_out_current_environment(self, read, mock_get, mock_patch):
        """
        Tests swap_in_available_environment_swap_out_current_environment CLI command.
        :param read:
        :param mock_get:
        :param mock_patch:
        """

        fake_get_responses = [mock.Mock(), mock.Mock(), mock.Mock()]
        fake_get_responses[0].status_code = 200
        fake_get_responses[0].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_get_responses[1].status_code = 200
        fake_get_responses[1].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_get_responses[2].status_code = 200
        fake_get_responses[2].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_patch_responses = [mock.Mock(), mock.Mock()]
        fake_patch_responses[0].status_code = 200
        fake_patch_responses[0].json.return_value = VALID_TEST_ENVIRONMENT_PATCH_RESPONSE
        fake_patch_responses[1].status_code = 200
        fake_patch_responses[1].json.return_value = VALID_TEST_ENVIRONMENT_PATCH_RESPONSE
        read.return_value = VALID_ARTIFCAT_TEST_ENVIRONMENT_ID
        mock_get.side_effect = fake_get_responses
        mock_patch.side_effect = fake_patch_responses

        runner = CliRunner()
        result = runner.invoke(swap_in_available_environment_swap_out_current_environment,
                               [
                                "-t", "validTestEnvironment",
                                "-op", "validPool",
                                "-np", "newValidPool",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    @mock.patch.object(ArtifactProperties, 'read')
    def test_swap_in_available_environment_swap_out_current_environment_error(self, read, mock_get, mock_patch):
        """
        Tests swap_in_available_environment_swap_out_current_environment CLI command with error.
        :param read:
        :param mock_get:
        :param mock_patch:
        """

        fake_get_responses = [mock.Mock(), mock.Mock(), mock.Mock()]
        fake_get_responses[0].status_code = 200
        fake_get_responses[0].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_get_responses[1].status_code = 200
        fake_get_responses[1].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_get_responses[2].status_code = 200
        fake_get_responses[2].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_patch_responses = [mock.Mock(), mock.Mock()]
        fake_patch_responses[0].status_code = 200
        fake_patch_responses[0].json.return_value = VALID_TEST_ENVIRONMENT_PATCH_RESPONSE
        fake_patch_responses[1].status_code = 400
        fake_patch_responses[1].json.return_value = {'error'}
        read.return_value = VALID_ARTIFCAT_TEST_ENVIRONMENT_ID
        mock_get.side_effect = fake_get_responses
        mock_patch.side_effect = fake_patch_responses

        runner = CliRunner()
        result = runner.invoke(swap_in_available_environment_swap_out_current_environment,
                               [
                                "-t", "validTestEnvironment",
                                "-op", "validPool",
                                "-np", "newValidPool",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_swap_test_environment_pool(self, mock_get, mock_patch):
        """
        Tests swap_test_environment_pool CLI command.
        :param mock_get:
        :param mock_patch:
        """
        fake_get_responses = [mock.Mock(), mock.Mock(), mock.Mock()]
        fake_get_responses[0].status_code = 200
        fake_get_responses[0].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_get_responses[1].status_code = 200
        fake_get_responses[1].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_get_responses[2].status_code = 200
        fake_get_responses[2].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_patch_responses = [mock.Mock(), mock.Mock()]
        fake_patch_responses[0].status_code = 200
        fake_patch_responses[0].json.return_value = VALID_TEST_ENVIRONMENT_PATCH_RESPONSE
        fake_patch_responses[1].status_code = 200
        fake_patch_responses[1].json.return_value = VALID_TEST_ENVIRONMENT_PATCH_RESPONSE
        mock_get.side_effect = fake_get_responses
        mock_patch.side_effect = fake_patch_responses

        runner = CliRunner()
        result = runner.invoke(swap_test_environment_pool,
                               [
                                "-t", "validTestEnvironment",
                                "-op", "validPool",
                                "-np", "newValidPool",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_swap_test_environment_pool_error(self, mock_get, mock_patch):
        """
        Tests swap_test_environment_pool CLI command with error.
        :param mock_get:
        :param mock_patch:
        """

        fake_get_responses = [mock.Mock(), mock.Mock(), mock.Mock()]
        fake_get_responses[0].status_code = 200
        fake_get_responses[0].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_get_responses[1].status_code = 200
        fake_get_responses[1].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_get_responses[2].status_code = 200
        fake_get_responses[2].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_patch_responses = [mock.Mock(), mock.Mock()]
        fake_patch_responses[0].status_code = 200
        fake_patch_responses[0].json.return_value = VALID_TEST_ENVIRONMENT_PATCH_RESPONSE
        fake_patch_responses[1].status_code = 400
        fake_patch_responses[1].json.return_value = {'error'}
        mock_get.side_effect = fake_get_responses
        mock_patch.side_effect = fake_patch_responses

        runner = CliRunner()
        result = runner.invoke(swap_test_environment_pool,
                               [
                                "-t", "validTestEnvironment",
                                "-op", "validPool",
                                "-np", "newValidPool",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 1

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_update_freshest_standby_env_to_available_and_swap_its_pool(self, mock_get, mock_patch):
        """
        Tests update_freshest_standby_env_to_available_and_swap_its_pool CLI command.
        :param mock_get:
        :param mock_patch:
        """

        fake_get_responses = [mock.Mock(), mock.Mock(), mock.Mock()]
        fake_get_responses[0].status_code = 200
        fake_get_responses[0].json.return_value = [SAMPLE_VALID_POOL_WITH_STANDBY_ENV_ATTACHED]
        fake_get_responses[1].status_code = 200
        fake_get_responses[1].json.return_value = [SAMPLE_VALID_TEST_ENV_SET_TO_STANDBY]
        fake_get_responses[2].status_code = 200
        fake_get_responses[2].json.return_value = SAMPLE_VALID_TEST_ENV_SET_TO_STANDBY
        fake_patch_responses = [mock.Mock(), mock.Mock()]
        fake_patch_responses[0].status_code = 200
        fake_patch_responses[0].json.return_value = VALID_TEST_ENVIRONMENT_PATCH_RESPONSE
        fake_patch_responses[1].status_code = 200
        fake_patch_responses[1].json.return_value = VALID_TEST_ENVIRONMENT_PATCH_RESPONSE
        mock_get.side_effect = fake_get_responses
        mock_patch.side_effect = fake_patch_responses

        runner = CliRunner()
        result = runner.invoke(update_freshest_standby_env_to_available_and_swap_its_pool,
                               [
                                "-op", "validPool",
                                "-np", "newValidPool",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 0

    @mock.patch('rptrc.src.etc.request_retry.requests.patch')
    @mock.patch('rptrc.src.etc.request_retry.requests.get')
    def test_update_freshest_standby_env_to_available_and_swap_its_pool_error(self, mock_get, mock_patch):
        """
        Tests update_freshest_standby_env_to_available_and_swap_its_pool CLI command with error.
        :param mock_get:
        :param mock_patch:
        """

        fake_get_responses = [mock.Mock(), mock.Mock(), mock.Mock()]
        fake_get_responses[0].status_code = 200
        fake_get_responses[0].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_get_responses[1].status_code = 200
        fake_get_responses[1].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_get_responses[2].status_code = 200
        fake_get_responses[2].json.return_value = [VALID_SAMPLE_TEST_ENVIRONMENT]
        fake_patch_responses = [mock.Mock(), mock.Mock()]
        fake_patch_responses[0].status_code = 200
        fake_patch_responses[0].json.return_value = VALID_TEST_ENVIRONMENT_PATCH_RESPONSE
        fake_patch_responses[1].status_code = 400
        fake_patch_responses[1].json.return_value = {'error'}
        mock_get.side_effect = fake_get_responses
        mock_patch.side_effect = fake_patch_responses

        runner = CliRunner()
        result = runner.invoke(update_freshest_standby_env_to_available_and_swap_its_pool,
                               [
                                "-op", "validPool",
                                "-np", "newValidPool",
                                "--verbose",
                                "--dev_mode"
                               ])
        assert result.exit_code == 1
