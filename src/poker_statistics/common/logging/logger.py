__author__ = "Eyal Avny"
__date__ = "26-Jan-20"
__copyright__ = "Copyright (C) 2020 IXDen (https://www.ixden.com)"

import importlib.resources as resources
import logging
import logging.config

_LOGGER_PORT = 9999


def init_logger(service_name: str) -> None:
    logging.basicConfig(format=f"{service_name} %(asctime)s  %(levelname)s  [%(threadName)s]  %(message)s",
                        level=logging.INFO)

    _init_logging_server(service_name)


def log_error(message: str) -> None:
    logging.error(message)


def log_warning(message: str) -> None:
    logging.warning(message)


def log_info(message: str) -> None:
    logging.info(message)


def log_debug(message: str) -> None:
    logging.debug(message)


def log_exception(exception: Exception) -> None:
    logging.exception(exception)


def _init_logging_server(service_name: str) -> None:
    config_file = 'poker_statistics/common/logging/logging.conf'

    # Read the new config file
    logging.config.fileConfig(str(config_file))

    # Create and start listener on port 9999 for logging configuration input
    t = logging.config.listen(_LOGGER_PORT)

    t.start()
