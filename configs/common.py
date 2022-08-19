import os


class CommonConfig:
    LOG_CONFIG: str = os.environ.get('common_log_config', './configs/logging.json')