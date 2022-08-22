import os


class DbConfig:
    DRIVER: str = os.environ.get('db_driver', 'postgresql+psycopg2')
    USER: str = os.environ.get('db_user', 'postgres')
    PASSWORD: str = os.environ.get('db_password', '')
    HOST: str = os.environ.get('db_host', '127.0.0.1')
    PORT: int = os.environ.get('db_port', '')
    SID: str = os.environ.get('db_database', '')

    DSN: str = f'{DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{SID}'

    # DEBUG OPTIONS #
    ECHO_DB_QUERIES: bool = bool(int(os.environ.get('db_echo_db', False)))
    ECHO_CONNECTION_POOL: bool = bool(int(os.environ.get('db_echo_pool', False)))
