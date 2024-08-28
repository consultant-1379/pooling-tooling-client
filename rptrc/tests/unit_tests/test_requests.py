"""
Unit tests for requests.py
"""
import pytest

from rptrc.src.operators.requests import Requests

VALID_SAMPLE_REQUEST = {
    "id": "876asd9fh",
    "testEnvironmentId": "9876asrb12",
    "poolName": "theFunOne",
    "requestorDetails": {
        "name": "John Doe",
        "area": "Product Staging",
        "executionId": "https://spinnaker.rnd.gic.ericsson.se"
                       "/#/applications/product-e2e-cicd/executions"
                       "/details/01FTZPSYFZ7V3XWMME5BA358QT"
    },
    "status": "Queued"
}


@pytest.fixture(autouse=True)
def reset_valid_sample_request():
    """
    Ran before each test as the sample request is modified by the
    create_queued_request function present in certain tests
    """
    VALID_SAMPLE_REQUEST['requestorDetails']['executionId'] = 'https://spinnaker.rnd.gic.ericsson.se' \
                                                              '/#/applications/product-e2e-cicd/executions' \
                                                              '/details/01FTZPSYFZ7V3XWMME5BA358QT'


VALID_ABORT_REQUEST_RESPONSE = {
    "id": "ckuctyf5j00000ppcdfd16196",
    "testEnvironmentId": "",
    "poolName": "j",
    "requestorDetails": {
        "name": "jack",
        "area": "local test"
    },
    "status": "Aborted",
    "createdOn": "Mon, 04 Oct 2021 15:51:00 GMT",
    "modifiedOn": "Mon, 04 Oct 2021 15:51:19 GMT",
    "lastReservedAt": "Mon, 04 Oct 2021 15:51:19 GMT"
}

INVALID_ABORT_REQUEST_RESPONSE = {
    "error": "Retrieved request is undefined or the object is empty"
}


class TestRequests:
    """
    Class to run unit tests for requests.py
    """

    def test_get_request_with_id(self, monkeypatch):
        """
        Tests that we can get a request with an id
        :param monkeypatch:
        """
        requests = Requests(dev_mode=True, retry_timeout=7200)
        monkeypatch.setattr(requests, "get", lambda url: [VALID_SAMPLE_REQUEST])
        actual_queued_request = requests.get_request_with_id('dummy')
        assert actual_queued_request == VALID_SAMPLE_REQUEST

    def test_get_request_with_id_no_request_found(self, monkeypatch):
        """
        Tests that handle the scenario where we cannot find a request with the given ID
        :param monkeypatch:
        """
        requests = Requests(dev_mode=True, retry_timeout=7200)
        monkeypatch.setattr(requests, "get", lambda url: [])

        with pytest.raises(Exception) as exception:
            requests.get_request_with_id('dummy')
        expected_exception_value = \
            'No Request entity with ID dummy was found in RPT'
        assert str(exception.value) == expected_exception_value

    def test_create_queued_request(self, monkeypatch):
        """
        Tests that we can create a queued request
        :param monkeypatch:
        """
        requests = Requests(dev_mode=True, retry_timeout=7200)
        monkeypatch.setattr(requests, "post", lambda url, request_body: VALID_SAMPLE_REQUEST)
        monkeypatch.setattr(requests, "wait_for_the_queued_request_be_resolved",
                            lambda url: VALID_SAMPLE_REQUEST)
        actual_queued_request = requests.create_queued_request(VALID_SAMPLE_REQUEST)
        assert actual_queued_request == VALID_SAMPLE_REQUEST

    def test_create_queued_request_try_catch_no_execution_id(self):
        """
        Tests that the try/catch block correctly handles key error if no execution ID provided or other
        :param monkeypatch:
        """
        requests = Requests(dev_mode=True, retry_timeout=7200)
        VALID_SAMPLE_REQUEST['requestorDetails'].pop('executionId')
        with pytest.raises(Exception) as exception:
            requests.create_queued_request(VALID_SAMPLE_REQUEST)
        expected_exception_value = 'Error found in the request body. ' \
                                   'Failed to create a new queued request!'
        assert str(exception.value) == expected_exception_value

    def test_create_queued_request_try_catch_index_error(self):
        """
        Tests that the try/catch block correctly handles index error upon malformed pipeline execution URL
        :param monkeypatch:
        """
        requests = Requests(dev_mode=True, retry_timeout=7200)
        VALID_SAMPLE_REQUEST['requestorDetails']['executionId'] = 'single_string'
        with pytest.raises(Exception) as exception:
            requests.create_queued_request(VALID_SAMPLE_REQUEST)
        expected_exception_value = 'Error found in the request body. ' \
                                   'Failed to create a new queued request!'
        assert str(exception.value) == expected_exception_value

    def test_create_queued_request_no_posted_request_found(self, monkeypatch):
        """
        Tests that when we create a queued request, if it fails and no
        posted request is found in the response, we catch that error
        :param monkeypatch:
        """
        requests = Requests(dev_mode=True, retry_timeout=7200)
        monkeypatch.setattr(requests, "post", lambda url, request_body: {'error'})
        with pytest.raises(Exception) as exception:
            requests.create_queued_request(VALID_SAMPLE_REQUEST)
        expected_exception_value = 'Error found in the request response. ' \
                                   'Failed to create a new queued request!'
        assert str(exception.value) == expected_exception_value

    def test_wait_for_the_queued_request_be_resolved(self, monkeypatch):
        """
        Tests that we can wait for a queued request to be resolved successfully
        :param monkeypatch:
        """
        requests = Requests(dev_mode=True, retry_timeout=7200)
        reserved_request = VALID_SAMPLE_REQUEST
        reserved_request['status'] = 'Reserved'
        monkeypatch.setattr(requests, "get_request_with_id", lambda request_id: reserved_request)
        actual_reserved_request = requests.wait_for_the_queued_request_be_resolved('dummy')
        assert actual_reserved_request == reserved_request

    def test_wait_for_the_queued_request_be_resolved_request_timeout(self, monkeypatch):
        """
        Tests that when we wait for a queued request to be resolved, if it times out,
        we catch that error
        :param monkeypatch:
        """
        requests = Requests(dev_mode=True, retry_timeout=7200)
        timeout_request = VALID_SAMPLE_REQUEST
        timeout_request['status'] = 'Timeout'
        monkeypatch.setattr(requests, "get_request_with_id", lambda request_id: timeout_request)
        with pytest.raises(Exception) as exception:
            requests.wait_for_the_queued_request_be_resolved(VALID_SAMPLE_REQUEST)
        expected_exception_value = \
            'Request timed out, there are no available environments. Please try again'
        assert str(exception.value) == expected_exception_value

    def test_abort_request_by_id_invalid_id_passed(self, monkeypatch):
        """
        Tests that when we abort a request with an invalid ID,
        an exception is raised.
        :param monkeypatch:
        """
        requests = Requests(dev_mode=True, retry_timeout=7200)
        monkeypatch.setattr(requests, "patch", lambda patch_url, request_body: INVALID_ABORT_REQUEST_RESPONSE)
        with pytest.raises(Exception) as exception:
            requests.abort_request_by_id('invalid_id_here')
        expected_exception_value = \
            'Error found in the request response. Failed to abort request, please contact Thunderbee.'
        assert str(exception.value) == expected_exception_value

    def test_abort_request_by_id_valid_id_passed(self, monkeypatch):
        """
        Test that when we abort a request with a valid ID, a
        valid abort request response is returned.
        :param monkeypatch:
        """
        requests = Requests(dev_mode=True, retry_timeout=7200)
        monkeypatch.setattr(requests, "patch", lambda patch_url, request_body: VALID_ABORT_REQUEST_RESPONSE, )
        response = requests.abort_request_by_id('ckuctyf5j00000ppcdfd16196')
        assert response == VALID_ABORT_REQUEST_RESPONSE
