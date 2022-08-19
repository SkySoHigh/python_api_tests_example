import json
import logging.config
from collections.abc import Callable
from typing import TypeVar, NoReturn, Any

from configs import CommonConfig

C = TypeVar('C', bound=Callable)

import logging
import allure

HANDLERS = logging.getLogger().handlers


class AllureLogger(logging.Handler):
    def emit(self, record):
        with allure.step(f'LOG ({record.levelname}): {record.getMessage()}'):
            pass


def log_func_call(function: C) -> C:
    """
    A type-safe decorator to add logging to a function.
    If there is 'allure' handler among all logger handlers - wraps logging output with allure.step()
    """

    def _log(*args, **kwargs):
        logging.info(f'func: "{function}", args: "{args}", kwargs: "{kwargs}"')

    def decorator(*args, **kwargs):
        if 'allure' in [h.name for h in HANDLERS]:
            with allure.step(f'Called: {function.__name__}'):
                _log(args, kwargs)
                return function(*args, **kwargs)
        else:
            _log(args, kwargs)
            return function(*args, **kwargs)

    return decorator


def setup_logging(logging_cfg_path: str):
    """
    Sets logger based on logging.json config
    Adds AllureLogger extension if 'allure' handler is present among all logger handlers

    Args:
        logging_cfg_path: Path to logging.json file

    Returns: NoReturn

    """
    try:
        with open(logging_cfg_path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)

        _logger = logging.getLogger()
        if 'allure' in [h.name for h in _logger.handlers]:
            _logger.addHandler(AllureLogger())

    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise e


class RequestHooks:
    @staticmethod
    def _emmit(title: str, log: Callable):
        if 'allure' in [h.name for h in HANDLERS]:
            with allure.step(title):
                log()
        else:
            log()

    @staticmethod
    def request_logging_hook(request: Any) -> NoReturn:
        """
        Adds logging for to outgoing request
        If there is 'allure' handler among all logger handlers - wraps logging output with allure.step()
        Args:
            request: Request object

        Returns: NoReturn

        """

        def _log():
            try:
                logging.info(f'URL: {request.method} {request.url}')
                logging.info(f'Headers: {request.headers}')
                logging.info(f'Content: {request.content}')
            except Exception as e:
                logging.warning(f'Exception occurred trying to access request params: {e}')
                pass

        RequestHooks._emmit(title='Request info', log=_log)

        return request

    @staticmethod
    def response_logging_hook(response: Any) -> NoReturn:
        """
        Adds logging for to outgoing request
        If there is 'allure' handler among all logger handlers - wraps logging output with allure.step()
        Args:
            response: Response object

        Returns: NoReturn
        """

        def _log():
            try:
                response.read()
                logging.info(f'URL: {response.url} {response.status_code}')
                logging.info(f'Headers: {response.headers}')
                logging.info(f'Cookies: {response.cookies}')
                logging.info(f'Content: {response.text}')
            except Exception as e:
                logging.warning(f'Exception occurred trying to access response params: {e}')
                pass

        RequestHooks._emmit(title='Response info', log=_log)

        return response


setup_logging(CommonConfig.LOG_CONFIG)
