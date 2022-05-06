# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, Query
from sqlalchemy.pool import QueuePool


@event.listens_for(Query, "before_compile", retval=True)
def refresh_info_in_session(query):
    return query.populate_existing()


class DBSession:

    def __init__(self, url: str, pool_size: int = 5, max_overflow: int = 5):
        """Database session constructor.

        Args:
            url (str): Database connection string (DSN). Example format: {DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{SID}
            pool_size (int, optional): Number of connections to be maintained. Defaults to 5.
            max_overflow (int, optional): The maximum overflow size of the pool. Defaults to 5.
        """
        self.__engine = create_engine(url,
                                      poolclass=QueuePool,
                                      pool_size=pool_size,
                                      max_overflow=max_overflow)
        self.__session = Session(self.__engine, future=True)

    @property
    def session(self):
        return self.__session

    @property
    def engine(self):
        return self.__engine
