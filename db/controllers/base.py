# -*- coding: utf-8 -*-
from typing import List, Type, Generator, TypeVar, Generic, NoReturn

from configs.logger import log_func_call
from db.entities.base import BaseModel
from db.transport import DbTransport
from libs.generic_types_helpers import get_generic_type_arg

DB_MODEL_TYPE = TypeVar("DB_MODEL_TYPE", bound=BaseModel)


class BaseDBController(Generic[DB_MODEL_TYPE]):
    """
    Contains a basic set of private methods for performing operations with database objects.
    """

    def __init__(self, transport: DbTransport):
        """
        Args:
            transport: SqlAlchemyTransport object for executing commands in the database (transport layer).
        """
        self.model = get_generic_type_arg(self)[0]
        self.transport = transport

    @log_func_call
    def create(self, entity: Type[DB_MODEL_TYPE]) -> NoReturn:
        """
        Adds object to the database.
        Args:
            entity: Object created on the basis of the table model.

        Returns: NoReturn
        """

        with self.transport.session_manager() as session:
            session.add(entity)
            session.commit()
            # Expunge object after it was created
            # https://docs.sqlalchemy.org/en/14/orm/session_state_management.html#expunging
            session.refresh(entity)
            session.expunge(entity)

    @log_func_call
    def read_by(self, *, limit: int = 1000, **filter_kwargs, ) -> List[DB_MODEL_TYPE]:
        """
        Reads model based objects from the database with provided filter_kwargs.

        Args:
            limit: Max query limit
            **filter_kwargs: Kwargs passed to the filter method (table columns and values).
                             If no filters are specified, then all objects will be returned.

        Returns: List with model based database objects

        """
        with self.transport.session_manager() as session:
            return session.query(self.model).filter_by(**filter_kwargs).limit(limit).all()

    @log_func_call
    def read_in_batches(self, *, batch_size: int = 100, **filter_kwargs) -> Generator[DB_MODEL_TYPE, None, None]:
        """
        Reads model based objects from the database as Generator.

        Args:
            batch_size: Max number of objects returned from the database per iteration.
            **filter_kwargs: Kwargs passed to the filter method (table columns and values).
                             If no filters are specified, then all objects will be returned.

        Returns: Generator with model based database objects
        """
        with self.transport.session_manager() as session:
            for r in session.query(self.model).filter_by(**filter_kwargs).yield_per(batch_size):
                yield r

    @log_func_call
    def update_by(self, where: dict, values: dict) -> NoReturn:
        with self.transport.session_manager() as session:
            session.query(self.model).filter_by(**where).update(values)
            session.commit()

    @log_func_call
    def delete(self, entity: Type[DB_MODEL_TYPE]) -> NoReturn:
        """
        Deletes object from the database.

        Args:
            entity: Object created on the basis of the table model.

        Returns: NoReturn
        """
        with self.transport.session_manager() as session:
            session.delete(entity)
            session.commit()

    @log_func_call
    def delete_by(self, **filter_kwargs) -> NoReturn:
        """
        Deletes all objects from the database with provided filter_kwargs.
        Args:
            **filter_kwargs: Kwargs passed to the filter method (table columns and values).
                             If no filters are specified, then all objects will be deleted.

        Returns: NoReturn
        """
        with self.transport.session_manager() as session:
            session.query(self.model).filter_by(**filter_kwargs).delete()
            session.commit()
