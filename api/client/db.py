from api.controllers.db import UserExampleDBController
from api.transport.db import DBSession
from config import ECHO_DB_QUERIES, ECHO_CONNECTION_POOL


class DBClient:
    def __init__(self, url: str, pool_size: int = 5, max_overflow: int = 5, echo: bool = ECHO_DB_QUERIES,
                 echo_pool: bool = ECHO_CONNECTION_POOL):
        """Database client, which provides access for all db controllers and methods.

        Args:
            url (str): Database connection string (DSN). Example format: {DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{SID}
            pool_size (int, optional): Number of connections to be maintained. Defaults to 5.
            max_overflow (int, optional): The maximum overflow size of the pool. Defaults to 5.
            echo (boolean, optional): if True, the Engine will log all statements.
            echo_pool (boolean, optional): if True, the connection pool will log informational output such as
            when connections are invalidated as well as when connections are recycled.
        """

        self.__db_session = DBSession(url=url,
                                      pool_size=pool_size,
                                      max_overflow=max_overflow,
                                      echo=echo,
                                      echo_pool=echo_pool)
        self.users = UserExampleDBController(self.__db_session)

    @property
    def db_params(self) -> DBSession:
        return self.__db_session
