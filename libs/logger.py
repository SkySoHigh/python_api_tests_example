import json
import logging.config
import os
import sys
from typing import Callable
from typing import TypeVar

_python_version = sys.version_info

if _python_version >= (3, 9):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

T = TypeVar('T')
P = ParamSpec('P')

logger = logging.getLogger(__name__)


def debug(f: Callable[P, T]) -> Callable[P, T]:
    """
    A type-safe decorator to add logging to a function.
    Note: Works ONLY with functions (not class methods).
    """

    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        kwstr = ', '.join('%r: %r' % (k, kwargs[k]) for k in sorted(kwargs))
        logger.debug(f'Calling {f.__name__} with args: {args} and kwargs: {kwstr}')
        return f(*args, **kwargs)

    return inner


def setup_logging(logging_cfg_path: str):
    """
    Sets logger based on logging.json config

    Args:
        logging_cfg_path: Path to logging.json file

    Returns: NoReturn

    """
    try:
        with open(logging_cfg_path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise e
