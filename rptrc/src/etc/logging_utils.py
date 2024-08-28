"""
Utilities file to store logging functions
"""
import logging


def initialize_logging(verbose=False, logging_identifier=None):
    """
    Get the Root Logger and Set the Handlers and the Formatters
    :param verbose: Flag to set logging level to debug
    :param logging_identifier: Identifier used for logging messages for Jenkins Build Failure Analysis
    """
    logger = logging.getLogger('')
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        log_format = '[%(levelname)s][%(filename)s:%(funcName)s:%(lineno)s][%(asctime)s] %(message)s'
        if logging_identifier is not None:
            log_format = (f'[%(levelname)s][%(filename)s:%(funcName)s:%(lineno)s][%(asctime)s][{logging_identifier}]'
                          ' %(message)s')
        formatter = logging.Formatter(log_format)
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)
        logger.addHandler(console)
    set_logging_verbosity_level(logger, verbose)


def set_logging_verbosity_level(logger, verbose):
    """
    Sets the verbosity level of the specified logger handler depending on the verbose
    option passed in
    :param logger: The logger to set the handler level for
    :param verbose: True or False
    """
    console = logger.handlers[0]
    if verbose:
        console.setLevel(logging.DEBUG)
        logging.debug("Logging Level set to DEBUG")
    else:
        console.setLevel(logging.INFO)
        logging.info("Logging Level set to INFO")
