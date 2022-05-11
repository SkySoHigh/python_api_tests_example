from api.controllers.db import UserDBController
from api.transport.db import DBSession


class DBClient:
    def __init__(self, url: str, pool_size: int = 5, max_overflow: int = 5):
        """Database client, which provides access for all db controllers and methods.

        Args:
            url (str): Database connection string (DSN). Example format: {DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{SID}
            pool_size (int, optional): Number of connections to be maintained. Defaults to 5.
            max_overflow (int, optional): The maximum overflow size of the pool. Defaults to 5.
        """

        self.__db_session = DBSession(url=url,
                                      pool_size=pool_size,
                                      max_overflow=max_overflow)
        self.users = UserDBController(self.session)

    @property
    def session(self):
        return self.__db_session.session

    @property
    def engine(self):
        return self.__db_session.engine

    @property
    def session_state(self):
        return {
            'new': self.session.new,
            'dirty': self.session.dirty,
            'deleted': self.session.deleted
        }
