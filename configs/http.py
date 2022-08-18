
class HttpConfig:
    PROTOCOL: str = 'http'
    HOST: str = '192.168.126.248'
    PORT: int = 8083
    BASE_ENDPOINT: str = ''

    USERNAME: str = 'admin'
    PASSWORD: str = 'elephant'

    URL: str = f'{PROTOCOL}://{HOST}:{PORT}/{BASE_ENDPOINT}'
    DEFAULT_HEADERS: dict = {}
    DEFAULT_COOKIES: dict = {}

    FOLLOW_REDIRECTS: bool = True
