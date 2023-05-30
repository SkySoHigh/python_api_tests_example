import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, SecretStr


class CommonConfig(BaseSettings):
    log_config: str = os.path.join(Path(__file__).resolve().parent, 'logging.json')

    class Config:
        env_prefix = 'common.'
        env_file = os.path.join(str(Path(__file__).parent.parent), '.env')


#
class DbConfig(BaseSettings):
    driver: str
    user: str
    password: SecretStr
    host: str
    port: int
    sid: str
    # DEBUG OPTIONS #
    echo_db_queries: bool = bool(int(os.environ.get('db_echo_db', False)))
    echo_connection_pool: bool = bool(int(os.environ.get('db_echo_pool', False)))

    @property
    def dsn(self) -> str:
        return f'{self.driver}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.sid}'

    class Config:
        env_prefix = 'db.'
        env_file = os.path.join(str(Path(__file__).parent.parent), '.env')


#
class HttpConfig(BaseSettings):
    url: str
    username: str
    password: SecretStr
    headers: dict
    cookies: dict
    follow_redirects: bool

    class Config:
        env_prefix = 'http.'
        env_file = os.path.join(str(Path(__file__).parent.parent), '.env')


#
class ConfigProvider(BaseSettings):
    http: HttpConfig = HttpConfig()
    db: DbConfig = DbConfig()
    common: CommonConfig = CommonConfig()


@lru_cache()
def get_configs() -> ConfigProvider:
    return ConfigProvider()
