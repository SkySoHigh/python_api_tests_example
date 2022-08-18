# -*- coding: utf-8 -*-
import logging
from typing import List, Type, Generator, TypeVar, Generic, NoReturn, Tuple

import allure

from api.transport.db import DbTransport
from libs.generic_types_helpers import get_generic_type_arg
from models.db import BaseModel

MODEL_TYPE = TypeVar("MODEL_TYPE", bound=BaseModel)


class BaseDBController(Generic[MODEL_TYPE]):
    """
    Contains a basic set of private methods for performing operations with database objects.
    """

    def __init__(self, transport: DbTransport):
        """
        Args:
            transport: SqlAlchemyTransport object for executing commands in the database (transport layer).
        """
        self.__model = get_generic_type_arg(self)[0]
        self.__session = transport.session_manager


    def create(self, entity: Type[MODEL_TYPE]) -> NoReturn:
        logging.info('Creaing: ')
        """
        Adds object to the database.
        Args:
            entity: Object created on the basis of the table model.

        Returns: NoReturn
        """

        with self.__session() as session:
            session.add(entity)
            session.commit()

    def read_by(self, *, limit: int = 1000, **filter_kwargs, ) -> List[Tuple[MODEL_TYPE]]:
        """
        Reads model based objects from the database with provided filter_kwargs.

        Args:
            limit: Max query limit
            **filter_kwargs: Kwargs passed to the filter method (table columns and values).
                             If no filters are specified, then all objects will be returned.

        Returns: List with model based database objects

        """
        with self.__session() as session:
            return session.query(self.__model).filter_by(**filter_kwargs).limit(limit).all()

    def read_in_batches(self, *, batch_size: int = 100, **filter_kwargs) -> Generator[MODEL_TYPE, None, None]:
        """
        Reads model based objects from the database as Generator.

        Args:
            batch_size: Max number of objects returned from the database per iteration.
            **filter_kwargs: Kwargs passed to the filter method (table columns and values).
                             If no filters are specified, then all objects will be returned.

        Returns: Generator with model based database objects
        """
        with self.__session() as session:
            for r in session.query(self.__model).filter_by(**filter_kwargs).yield_per(batch_size):
                yield r

    def update_by(self, where: dict, values: dict) -> NoReturn:
        with self.__session() as session:
            session.query(self.__model).filter_by(**where).update(values)
            session.commit()

    def delete(self, entity: Type[MODEL_TYPE]) -> NoReturn:
        """
        Deletes object from the database.

        Args:
            entity: Object created on the basis of the table model.

        Returns: NoReturn
        """
        with self.__session() as session:
            session.delete(entity)
            session.commit()

    def delete_by(self, **filter_kwargs) -> NoReturn:
        """
        Deletes all objects from the database with provided filter_kwargs.
        Args:
            **filter_kwargs: Kwargs passed to the filter method (table columns and values).
                             If no filters are specified, then all objects will be deleted.

        Returns: NoReturn
        """
        with self.__session() as session:
            session.query(self.__model).filter_by(**filter_kwargs).delete()
            session.commit()
