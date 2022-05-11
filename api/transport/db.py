# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, Query
from sqlalchemy.pool import QueuePool


@event.listens_for(Query, "before_compile", retval=True)
def refresh_info_in_session(query):
    return query.populate_existing()


class DBSession:

    def __init__(self, url: str, pool_size: int = 5, max_overflow: int = 5, echo: bool = False,
                 echo_pool: bool = False):
        """Database session constructor.

        Args:
            url (str): Database connection string (DSN). Example format: {DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{SID}
            pool_size (int, optional): Number of connections to be maintained. Defaults: 5.
            max_overflow (int, optional): The maximum overflow size of the pool. Defaults: 5.
            echo (boolean, optional): if True, the Engine will log all statements. Defaults: False
            echo_pool (boolean, optional): if True, the connection pool will log informational output such as
            when connections are invalidated as well as when connections are recycled. Defaults: False
        """
        self.__engine = create_engine(url,
                                      poolclass=QueuePool,
                                      pool_size=pool_size,
                                      max_overflow=max_overflow,
                                      echo=echo,
                                      echo_pool=echo_pool)
        self.__session = Session(self.__engine, future=True)

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def engine(self):
        return self.__engine
