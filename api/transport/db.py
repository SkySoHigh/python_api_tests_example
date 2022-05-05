# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, event, delete, insert, select, update
from sqlalchemy.orm import Session, Query
from sqlalchemy.pool import QueuePool

# For type hinting
from sqlalchemy.sql.dml import Delete, Insert, Update
from sqlalchemy.sql.selectable import Select


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

    def close(self):
        self.__session.close()
        self.__engine.dispose()

    def execute(self, statement, **kwargs):
        return self.__session.execute(statement, **kwargs)

    def query(self, *entities, **kwargs) -> Query:
        return self.__session.query(*entities, **kwargs)

    def update(self, entity) -> Update:
        return update(entity)

    def insert(self, entity) -> Insert:
        return insert(entity)

    def delete(self, entity) -> Delete:
        return delete(entity)

    def select(self, entity) -> Select:
        return select(entity)

    def commit(self):
        return self.__session.commit()
