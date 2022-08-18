from httpx import Client, Response


class HttpTransport(Client):
    pass


class HttpResponse(Response):
    """
    This class exists for only one reason: we need it to provide type hinting.
    You can ask a good question: why can't I import Response from httpx where I need it? Let me explain.
    HTTPResponse inherits class Response from httpx library now, but later we can switch to another library. So, we can
    fix import here and import of this class stays the same way it is now.
    """