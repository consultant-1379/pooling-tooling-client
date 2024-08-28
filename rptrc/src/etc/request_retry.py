"""
This module allows a user to attempt to make a request multiple times if the target host is
temporarily down
"""

import logging
from time import sleep
import requests
import urllib3

from rptrc.src.etc.exceptions import FatalException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SLEEP_TIME_MULTIPLIER = 5


# pylint: disable=no-member, too-many-arguments
def request_retry(type_of_request, url, retry_timeout, body=None, proxy=None, ssl=False):
    """
    Function to retry requests if the target host is not found. Geometric retry is used here.
    :param type_of_request: Which REST request is being conducted
    :param url: URL you want to run your request against
    :param retry_timeout: The total sleep time of a request retry
    :param body: The payload which will be sent in the request body
    :param proxy: Proxy dict if you would like to route request through proxy
    :param ssl: Should be set to True if you want to enable SSL verification.
    :return: response
    :rtype: requests.Response
    """
    count = 0
    response = None
    max_retry = calculate_max_retry_based_on_retry_timeout(retry_timeout)
    valid_response_codes = [requests.codes.ok, requests.codes.created]
    logging.debug(f"type_of_request: {str(type_of_request)}")
    logging.debug(f"url: {str(url)}")
    while count < max_retry:
        try:
            response = make_request_based_on_input(type_of_request, url, body, proxy, ssl)
            if response and response.status_code in valid_response_codes:
                break
            raise requests.exceptions.RequestException
        except Exception:
            logging.error(f"Could not make the {type_of_request} request")
            if response is not None:
                logging.error(f"Response status code: {str(response.status_code)}")
                logging.error(f"Response reason: {str(response.reason)}")
                logging.error(f"Response output: {str(response.text)}")
                handle_response_exception(response=response)

        count += 1
        if count == max_retry:
            exception_message = f"Failed to execute {type_of_request} request after {max_retry} tries."
            logging.critical(exception_message)
            raise FatalException(exception_message)

        logging.warning(f"Failed to make {type_of_request} request. "
                        f"Sleeping and then trying again...")
        sleep(SLEEP_TIME_MULTIPLIER * count)
    return response


def calculate_max_retry_based_on_retry_timeout(retry_timeout):
    """
    Function to calculate the amount of retries needed based on the retry timeout passed to the request_retry function
    :param retry_timeout
    :return: retry_count-1
    """
    retry_count = 1
    total_time_slept = 0
    while total_time_slept <= retry_timeout:
        total_time_slept += SLEEP_TIME_MULTIPLIER * retry_count
        retry_count += 1

    return retry_count-1


def handle_response_exception(response):
    """
    Function to handle the exceptions raised due to Response
    :param response:
    """
    if response.status_code == requests.codes.bad_request:
        exception_message = "Bad request detected. It is possible you may be missing " \
                            "required information in your request. Please see above."
        logging.error(exception_message)
        raise requests.exceptions.RequestException(exception_message)

    if response.status_code == requests.codes.internal_server_error:
        exception_message = "Error thrown by RPT. The request could not be processed."
        logging.error(exception_message)
        raise requests.exceptions.RequestException(exception_message)


def make_request_based_on_input(request_type, url, body, proxy, ssl):
    """
    Makes a request based on the request type passed in
    :param request_type: Which REST request is being conducted
    :param url: URL you want to run your request against
    :param body: The payload which will be sent in the request body
    :param proxy: Proxy dict if you would like to route request through proxy
    :return: response
    :rtype: requests.Response
    """
    logging.debug(f"Trying to make {request_type} request")
    response = None
    try:
        if request_type == "GET":
            logging.debug("Doing a GET request")
            response = requests.get(url, proxies=proxy, timeout=10, verify=ssl)
        elif request_type == "PATCH":
            logging.debug("Doing a PATCH request")
            response = requests.patch(url, json=body, timeout=20, proxies=proxy, verify=ssl)
        elif request_type == "PUT":
            logging.debug("Doing a PUT request")
            response = requests.put(url, json=body, timeout=5, proxies=proxy, verify=ssl)
        elif request_type == "POST":
            logging.debug("Doing a POST request")
            response = requests.post(url, json=body, timeout=20, proxies=proxy, verify=ssl)
        elif request_type == "DELETE":
            logging.debug("Doing a DELETE request")
            response = requests.delete(url, timeout=10, proxies=proxy, verify=ssl)
        else:
            exception_message = f"Unsupported type of request: {request_type}"
            logging.critical(exception_message)
            raise FatalException(exception_message)
    except (requests.exceptions.ProxyError, AssertionError):
        logging.error(f"Could not make {request_type} request due to a Proxy Error")
    return response
