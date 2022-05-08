import logging
import logging.config
import os
import json

from decorator import decorator

logger = logging.getLogger(__name__)


@decorator
def debug(f, *args, **kw):
    """
    Logs all function calls on a DEBUG log level
    Args:
        f: Decorated function
        *args: Decorated function args
        **kw: Decorated function kwargs

    Returns:

    """
    kwstr = ', '.join('%r: %r' % (k, kw[k]) for k in sorted(kw))
    logger.debug(f'Calling {f.__name__} with args: {args} and kwargs: {kwstr}')
    return f(*args, **kw)


def setup_logging(default_path="./logging.json", env_key="LOG_CFG"):
    """
    Sets logger based on logging.json config

    Args:
        default_path: Path to logging.json file
        env_key: ENV variable with path to logging.json file

    Returns: NoReturn

    """
    env_value = os.getenv(env_key, None)
    path = default_path if not env_value else env_value
    try:
        with open(path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise e
