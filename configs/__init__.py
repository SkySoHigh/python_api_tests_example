from config import get_configs
from configs.logger import setup_logging

# Config provider
ConfigProvider = get_configs()

# Setup global logging handlers for allure
setup_logging(ConfigProvider.common.log_config)
