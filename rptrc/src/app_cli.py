"""
This is the CLI for the Pooling Tooling REST client.
"""
import json
import logging

import click

from rptrc.src.etc import logging_utils
from rptrc.src.etc.exceptions import FatalException
from rptrc.src.operators.property_converter import PropertyConverter
from rptrc.src.operators.requests import Requests
from rptrc.src.operators.test_environments import TestEnvironments
from rptrc.src.operators.artifact_properties import ArtifactProperties
from rptrc.src.operators.pools import Pools


def log_verbose_option(func):
    """A decorator for the log verbose command line argument."""
    return click.option('-v', '--verbose', type=click.BOOL, is_flag=True, required=False,
                        help='Increase output verbosity')(func)


def dev_mode_option(func):
    """A decorator for the dev_mode command line argument."""
    return click.option('--dev_mode', type=click.BOOL, is_flag=True, required=False,
                        help='Run tool in development mode against RPT staging')(func)


def print_to_console_option(func):
    """A decorator for the print_to_console command line argument."""
    return click.option('-p', '--print_to_console', type=click.BOOL, is_flag=True, required=False,
                        help='Option to output the value to console in order to be capture by '
                             'other scripts e.g. bash scripts')(func)


def request_body_option(func):
    """A decorator for the request_body command line argument."""
    return click.option('-b', '--request_body', type=click.STRING, required=True,
                        help='Request body. Should be JSON in string format.')(func)


def pool_name_option(func):
    """A decorator for the pool_name command line argument."""
    return click.option('-pl', '--pool_name', type=click.STRING, required=True,
                        help='Pool name.')(func)


def test_environment_name_option(func):
    """A decorator for the test_environment_name command line argument."""
    return click.option('-t', '--test_environment_name', type=click.STRING, required=True,
                        help='Test environment name.')(func)


def entity_id_option(func):
    """A decorator for the entity_id command line argument."""
    return click.option('-id', '--entity_id', type=click.STRING, required=True,
                        help='The ID of the entity. Used in functions like updating an '
                             'entity')(func)


def pipeline_stage_option(func):
    """A decorator for the pipeline_stage command line argument."""
    return click.option('-ps', '--pipeline_stage', type=click.STRING, required=True,
                        help='The pipeline stage that is currently using a test '
                             'environment.')(func)


def generate_artifact_properties_option(func):
    """A decorator for the generate_artifact_properties command line argument."""
    return click.option('-gap', '--generate_artifact_properties', type=click.BOOL, is_flag=True, required=False,
                        help='Option to generate the artifact.properties file for use by '
                             'Spinnaker pipelines.')(func)


def pool_to_swap_environment_from_option(func):
    """A decorator for the pool_to_swap_environment_from command line argument."""
    return click.option('-op', '--pool_to_swap_environment_from', type=click.STRING,
                        required=False, help='Option to specify pool you want to '
                                             'swap the test environment from')(func)


def pool_to_swap_environment_to_option(func):
    """A decorator for the pool_to_swap_environment_to command line argument."""
    return click.option('-np', '--pool_to_swap_environment_to', type=click.STRING,
                        required=False, help='Option to specify pool you want to '
                                             'swap the test environment to')(func)


def version_to_compare_environment_against_option(func):
    """A decorator for the version_to_compare_environment_against command line argument."""
    return click.option('-vfc', '--version_for_comparison', type=click.STRING, required=True,
                        help='The version of helmfile to compare against the version currently '
                             'deployed on the environment')(func)


def logging_identifier_option(func):
    """A decorator for the logging_identifier command line argument."""
    return click.option('-li', '--logging_identifier', type=click.STRING, required=False,
                        help='The identifier to be included in log statements')(func)


def retry_timeout_option(func):
    """A decorator for the retry timeout command line argument"""
    return click.option('-rt', '--retry_timeout', type=click.INT, required=False, default=7200,
                        help='The timeout in seconds between retry requests if the target host is not found')(func)


@click.group()
def cli_main():
    """
    The entry-point to the Pooling Tooling REST client.
    Please see available options below.
    """


@cli_main.command()
@log_verbose_option
@dev_mode_option
@request_body_option
@pipeline_stage_option
@generate_artifact_properties_option
@logging_identifier_option
@retry_timeout_option
def create_queued_request(verbose,
                          dev_mode,
                          request_body: str,
                          pipeline_stage,
                          generate_artifact_properties,
                          retry_timeout,
                          logging_identifier=None,
                          ):
    """
    Creates an instance of the Request entity in RPT with a queued status.
    Then it waits for the request to be resolved or to timeout. If resolved
    it will generate the artifact.properties file containing the resource name.
    :param verbose:
    :param dev_mode:
    :param request_body:
    :param pipeline_stage:
    :param generate_artifact_properties:
    :param logging_identifier:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose, logging_identifier)
    requests = Requests(dev_mode, retry_timeout)
    request = requests.create_queued_request(json.loads(request_body))
    if generate_artifact_properties:
        artifact_properties = ArtifactProperties({'REQUEST_ID': request['id']})
        artifact_properties.generate()
    request = requests.wait_for_the_queued_request_be_resolved(request['id'])
    test_environment = TestEnvironments(dev_mode, retry_timeout, None)
    test_environment_patch_response = \
        test_environment.update_test_environment_stage(pipeline_stage, request['testEnvironmentId'])
    if generate_artifact_properties:
        test_environment_name = test_environment_patch_response["name"]
        artifact_properties = ArtifactProperties({'RESOURCE_NAME': test_environment_name}, mode='a')
        artifact_properties.generate()


@cli_main.command()
@log_verbose_option
@dev_mode_option
@retry_timeout_option
def abort_queued_request(verbose, dev_mode, retry_timeout):
    """
    Aborts a queued request using the ID stored in the local artifact.properties file.
    :param verbose:
    :param dev_mode:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)
    artifact_properties = ArtifactProperties()
    request_id = artifact_properties.read()['REQUEST_ID']
    requests_operator = Requests(dev_mode, retry_timeout)
    requests_operator.abort_request_by_id(request_id)


@cli_main.command()
@log_verbose_option
@dev_mode_option
@test_environment_name_option
@retry_timeout_option
def unreserve_environment(verbose, dev_mode, test_environment_name, retry_timeout):
    """
    Unreserves a test environment in RPT.
    :param verbose:
    :param dev_mode:
    :param test_environment_name:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)
    test_environment = TestEnvironments(dev_mode, retry_timeout, test_environment_name)
    test_environment.unreserve_test_environment()


@cli_main.command()
@log_verbose_option
@dev_mode_option
@test_environment_name_option
@retry_timeout_option
def quarantine_environment(verbose, dev_mode, test_environment_name, retry_timeout):
    """
    Quarantines a test environment in RPT.
    :param verbose:
    :param dev_mode:
    :param test_environment_name:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)
    test_environment = TestEnvironments(dev_mode, retry_timeout, test_environment_name)
    test_environment.quarantine_test_environment()


@cli_main.command()
@log_verbose_option
@dev_mode_option
@test_environment_name_option
@retry_timeout_option
def set_standby_environment_to_available(verbose, dev_mode, test_environment_name, retry_timeout):
    """
    Sets a standby test environment to available in RPT.
    :param verbose:
    :param dev_mode:
    :param test_environment_name:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)
    test_environment = TestEnvironments(dev_mode, retry_timeout, test_environment_name)
    test_environment.set_standby_test_environment_to_available()


@cli_main.command()
@log_verbose_option
@dev_mode_option
@test_environment_name_option
@pipeline_stage_option
@retry_timeout_option
def update_test_environment_stage(verbose, dev_mode, test_environment_name, pipeline_stage, retry_timeout):
    """
    Updates the stage of a test environment in RPT.
    :param verbose:
    :param dev_mode:
    :param test_environment_name:
    :param pipeline_stage:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)
    test_environment = TestEnvironments(dev_mode, retry_timeout, test_environment_name)
    test_environment.update_test_environment_stage(pipeline_stage)


@cli_main.command()
@log_verbose_option
@dev_mode_option
@test_environment_name_option
@request_body_option
@retry_timeout_option
def store_test_environment_details(verbose, dev_mode, test_environment_name, request_body, retry_timeout):
    """
    Updates the details/properties of a test environment in RPT.
    :param verbose:
    :param dev_mode:
    :param test_environment_name:
    :param request_body:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)
    test_environment = TestEnvironments(dev_mode, retry_timeout, test_environment_name)
    request_body_dict = json.loads(request_body)
    property_converter = PropertyConverter(request_body_dict)
    converted_request_body_dict = property_converter.convert_properties('uppercase_to_camelcase')
    converted_request_body = json.dumps(converted_request_body_dict)
    patch_url = f'{test_environment.test_environment_url}/' \
                f'{test_environment.retrieve_test_environment_by_name()["id"]}'
    test_environment.patch(patch_url, converted_request_body)


@cli_main.command()
@log_verbose_option
@dev_mode_option
@pool_name_option
@request_body_option
@retry_timeout_option
def store_details_for_test_environments_by_pool(verbose, dev_mode, pool_name, request_body, retry_timeout):
    """
    Updates the details/properties of all test environments in a specified pool in RPT.
    :param verbose:
    :param dev_mode:
    :param pool_name:
    :param request_body:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)
    pool = Pools(dev_mode, retry_timeout, pool_name)
    test_environments_in_pool = pool.retrieve_test_environments_by_pool(pool_name)

    request_body_dict = json.loads(request_body)
    property_converter = PropertyConverter(request_body_dict)
    converted_request_body_dict = property_converter.convert_properties('uppercase_to_camelcase')
    converted_request_body = json.dumps(converted_request_body_dict)

    for test_environment_id in test_environments_in_pool:
        test_environment = TestEnvironments(dev_mode, retry_timeout, test_environment_id=test_environment_id)
        patch_url = f'{test_environment.test_environment_url}/' \
                    f'{test_environment.retrieve_test_environment_by_id()["id"]}'
        test_environment.patch(patch_url, converted_request_body)


@cli_main.command()
@log_verbose_option
@dev_mode_option
@test_environment_name_option
@generate_artifact_properties_option
@retry_timeout_option
def retrieve_test_environment_details(verbose, dev_mode, test_environment_name,
                                      generate_artifact_properties, retry_timeout):
    """
    Retrieves the details/properties of a test environment in RPT.
    :param verbose:
    :param dev_mode:
    :param test_environment_name:
    :param generate_artifact_properties:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)
    test_environment = TestEnvironments(dev_mode, retry_timeout, test_environment_name)
    test_environment_details = test_environment.retrieve_test_environment_by_name()["properties"]
    property_converter = PropertyConverter(test_environment_details)
    converted_test_environment_details = property_converter.convert_properties('camelcase_to_uppercase')
    if generate_artifact_properties:
        artifact_properties = ArtifactProperties(converted_test_environment_details)
        artifact_properties.generate()


@cli_main.command()
@log_verbose_option
@dev_mode_option
@test_environment_name_option
@version_to_compare_environment_against_option
@retry_timeout_option
def fail_if_version_specified_equals_version_on_test_environment(verbose, dev_mode, test_environment_name,
                                                                 version_for_comparison, retry_timeout):
    """
    Checks if the "version" present on the test environment equals that which was passed in
    If they are the same, we raise an Exception and fail the pipeline as we believe the test
    environment is trying to deploy to the same version it is already on
    :param verbose:
    :param dev_mode:
    :param test_environment_name:
    :param version_for_comparison:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)
    test_environment = TestEnvironments(dev_mode, retry_timeout, test_environment_name)
    test_environment_details = test_environment.retrieve_test_environment_by_name()
    if test_environment_details['properties']['version'] == version_for_comparison:
        exception_message = ('Not continuing with pipeline as version on system is the same as '
                             'that passed into this job.')
        logging.critical(exception_message)
        raise FatalException(exception_message)


@cli_main.command()
@log_verbose_option
@dev_mode_option
@test_environment_name_option
@version_to_compare_environment_against_option
@generate_artifact_properties_option
@retry_timeout_option
def check_if_version_specified_equals_version_on_test_environment(verbose, dev_mode,
                                                                  test_environment_name,
                                                                  version_for_comparison,
                                                                  generate_artifact_properties,
                                                                  retry_timeout):
    """
    Checks if the "version" present on the test environment equals that which was passed in
    and generates artifact.properties file containing result of the check
    :param verbose:
    :param dev_mode:
    :param test_environment_name:
    :param version_for_comparison:
    :param generate_artifact_properties:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)
    test_environment = TestEnvironments(dev_mode, retry_timeout, test_environment_name)
    result_of_check_if_test_environment_on_specified_version = \
        test_environment.check_if_test_environment_on_specified_version(version_for_comparison)
    if generate_artifact_properties:
        artifact_properties = ArtifactProperties({"ENV_ON_LATEST_VERSION":
                                                  result_of_check_if_test_environment_on_specified_version})
        artifact_properties.generate()


@cli_main.command()
@log_verbose_option
@dev_mode_option
@pool_name_option
@generate_artifact_properties_option
@retry_timeout_option
def update_freshest_standby_test_environment_to_available(verbose, dev_mode, pool_name,
                                                          generate_artifact_properties, retry_timeout):
    """
    Updates the status of the freshest standby test environment to available in a specified
    pool in RPT and generates artifact.properties file containing the id of updated environment
    :param verbose:
    :param dev_mode:
    :param pool_name:
    :param generate_artifact_properties:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)

    pool = Pools(dev_mode, retry_timeout, pool_name)
    test_environments_in_pool_ids = pool.retrieve_test_environments_by_pool(pool_name)

    test_environment = TestEnvironments(dev_mode, retry_timeout)
    standby_test_environments_in_pool = test_environment \
        .retrieve_standby_test_environments(test_environments_in_pool_ids)

    standby_test_environments_in_pool_ids_string = ",".join(standby_test_environments_in_pool)

    freshest_standby_test_environment_in_pool = test_environment \
        .retrieve_freshest_test_environment(standby_test_environments_in_pool_ids_string)
    test_environment.test_environment_name = freshest_standby_test_environment_in_pool["name"]
    test_environment.set_standby_test_environment_to_available()

    if generate_artifact_properties:
        artifact_properties = ArtifactProperties({"AVAILABLE_TEST_ENVIRONMENT_ID":
                                                  freshest_standby_test_environment_in_pool["id"]})
        artifact_properties.generate()


@cli_main.command()
@log_verbose_option
@dev_mode_option
@test_environment_name_option
@pool_to_swap_environment_from_option
@pool_to_swap_environment_to_option
@retry_timeout_option
def swap_in_available_environment_swap_out_current_environment(verbose, dev_mode, test_environment_name,
                                                               pool_to_swap_environment_from,
                                                               pool_to_swap_environment_to, retry_timeout):
    """
    Swaps into destination pool, the environment with the id retrieved from the artifact.properties file
    and swaps out the named environment to the source pool.
    :param verbose:
    :param dev_mode:
    :param test_environment_name:
    :param pool_to_swap_environment_from:
    :param pool_to_swap_environment_to:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)
    pool = Pools(dev_mode, retry_timeout, 'new_pool')
    artifact_properties = ArtifactProperties()
    test_environment_id = artifact_properties.read()['AVAILABLE_TEST_ENVIRONMENT_ID']

    test_environment_to_swap_in = TestEnvironments(dev_mode, retry_timeout, test_environment_id=test_environment_id)
    test_environment_to_swap_in_pools = test_environment_to_swap_in.retrieve_test_environment_by_id()["pools"]

    updated_test_environment_to_swap_in_pools = pool.update_list_of_pools(
        test_environment_to_swap_in_pools, pool_to_swap_environment_from,
        pool_to_swap_environment_to)

    test_environment_to_swap_in.update_test_environment_pool(
        updated_test_environment_to_swap_in_pools, test_environment_id)

    test_environment_to_swap_out = TestEnvironments(dev_mode, retry_timeout,
                                                    test_environment_name=test_environment_name)
    test_environment_to_swap_out_pools = test_environment_to_swap_out.retrieve_test_environment_by_name()["pools"]

    updated_test_environment_to_swap_out_pools = pool.update_list_of_pools(
        test_environment_to_swap_out_pools, pool_to_swap_environment_to,
        pool_to_swap_environment_from)

    test_environment_to_swap_out.update_test_environment_pool(
        updated_test_environment_to_swap_out_pools, test_environment_to_swap_out.test_environment_id)


@cli_main.command()
@log_verbose_option
@dev_mode_option
@test_environment_name_option
@pool_to_swap_environment_from_option
@pool_to_swap_environment_to_option
@retry_timeout_option
def swap_test_environment_pool(verbose, dev_mode, test_environment_name, pool_to_swap_environment_from,
                               pool_to_swap_environment_to, retry_timeout):
    """
    Swaps the pool of the environment passed in
    :param verbose:
    :param dev_mode:
    :param test_environment_name:
    :param pool_to_swap_environment_from:
    :param pool_to_swap_environment_to:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)
    pool = Pools(dev_mode, retry_timeout, 'new_pool')
    test_env_to_swap_out_of_pool = TestEnvironments(dev_mode, retry_timeout,
                                                    test_environment_name=test_environment_name)
    info_of_test_env_to_swap_out_of_pool = test_env_to_swap_out_of_pool.retrieve_test_environment_by_name()
    list_of_pools_attached_to_env = pool.update_list_of_pools(
        info_of_test_env_to_swap_out_of_pool['pools'], pool_to_swap_environment_from, pool_to_swap_environment_to)
    test_env_to_swap_out_of_pool.update_test_environment_pool(
        list_of_pools_attached_to_env, info_of_test_env_to_swap_out_of_pool["id"])


@cli_main.command()
@log_verbose_option
@dev_mode_option
@pool_to_swap_environment_from_option
@pool_to_swap_environment_to_option
@generate_artifact_properties_option
@retry_timeout_option
def update_freshest_standby_env_to_available_and_swap_its_pool(verbose, dev_mode, pool_to_swap_environment_from,
                                                               pool_to_swap_environment_to,
                                                               generate_artifact_properties, retry_timeout):
    """
    This will find the freshest standby environment in the specified pool.
    It will swap its status to Available and will swap the pool the environment is in
    :param verbose:
    :param dev_mode:
    :param pool_to_swap_environment_from:
    :param pool_to_swap_environment_to:
    :param generate_artifact_properties:
    :param retry_timeout:
    """
    logging_utils.initialize_logging(verbose)

    pool = Pools(dev_mode, retry_timeout, pool_to_swap_environment_from)
    test_envs_in_specified_pool = pool.retrieve_test_environments_by_pool(pool_to_swap_environment_from)

    test_env = TestEnvironments(dev_mode, retry_timeout)
    standby_test_environments_in_pool = test_env.retrieve_standby_test_environments(
        test_envs_in_specified_pool)

    standby_test_env_in_pool_ids_string = ','.join(standby_test_environments_in_pool)

    freshest_standby_test_env_in_pool = test_env.retrieve_freshest_test_environment(
        standby_test_env_in_pool_ids_string)

    test_env.test_environment_name = freshest_standby_test_env_in_pool['name']

    test_env.set_standby_test_environment_to_available()

    updated_list_of_pools = pool.update_list_of_pools(
        freshest_standby_test_env_in_pool['pools'], pool_to_swap_environment_from, pool_to_swap_environment_to)
    test_env.update_test_environment_pool(updated_list_of_pools, freshest_standby_test_env_in_pool['id'])

    if generate_artifact_properties:
        artifact_properties = ArtifactProperties({"SWAPPED_IN_TEST_ENVIRONMENT_NAME":
                                                  test_env.test_environment_name})
        artifact_properties.generate()
