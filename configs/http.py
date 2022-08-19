import json
import os


class HttpConfig:
    PROTOCOL: str = os.environ.get('http_protocol', 'http')
    HOST: str = os.environ.get('http_host', '')
    PORT: int = os.environ.get('http_port', '')
    BASE_ENDPOINT: str = os.environ.get('http_base_endpoint', '/')

    USERNAME: str = os.environ.get('http_username', 'username')
    PASSWORD: str = os.environ.get('http_password', 'password')

    URL: str = f'{PROTOCOL}://{HOST}:{PORT}/{BASE_ENDPOINT}'

    DEFAULT_HEADERS: dict = json.loads(os.environ.get('http_headers', '').replace("'", "\""))
    DEFAULT_COOKIES: dict = json.loads(os.environ.get('http_cookies', '').replace("'", "\""))

    FOLLOW_REDIRECTS: bool = bool(int(os.environ.get('http_follow_redirects', True)))
