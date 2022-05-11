# -*- coding: utf-8 -*-
import abc
from abc import ABC
from typing import List, Optional, Type, Generator, Any

from decorator import decorator
from sqlalchemy.orm import Session

from libs.logging import debug
from models.db import AbcDBModel


@decorator
def default(func, name: str = None, *args, **kwargs):
    """
    Decorates unimplemented methods of descendants of the BaseDBController class to call their encapsulated equivalent
    from the base class with a redefined call signature and typehints.
    Mapping of functions occurs by the same name with the prefix "_".

    Example:
    ... class MyCustomController(BaseDBController):
    ...    @default
    ...    def create(self, entity: Type[User]) -> None: pass
    ...    # BaseDBController._create(...) would be used

    Args:
        func: Decorated function
        name: Name of the function in the BaseDBController. If empty: '_' + func.__name__  will be used.
        *args: Decorated function args (declared in the interface)
        **kwargs: Decorated function kwargs (declared in the interface)

    Returns: Original function from BaseDBController decorated with interface signature and typehints
    """

    try:
        name = name if name else f'_{func.__name__}'
        self, args = args[0], args[1::]
        def_func = getattr(self, str(name))
        return def_func(*args, **kwargs)
    except AttributeError:
        raise AttributeError(f'There is no default implementation with name: {name} '
                             f'among BaseDBController methods')


def default_all(cls):
    """
    Decorates all class method with '@default' decorator.
    Warning: If there is @default decorator on a method and @default_all on a class,
    then only the latter will have an effect.

    Example:
    ... @default_all
    ... class MyCustomController(BaseDBController):
    ...    def create(self, entity: Type[User]) -> None: pass
    ...    # BaseDBController._create(...) would be used

    Returns: NoReturn
    """
    for attr in cls.__dict__:
        if callable(getattr(cls, attr)) and not attr.startswith("_"):
            setattr(cls, attr, default(getattr(cls, attr)))
    return cls


@decorator
def commit(function, self, *args, **kwargs) -> Any:
    """
    Sends a commit after successful execution of the request and performs a rollback in case of an error
    Args:
        function: Decorated function
        self: Class object with 'session' property
        *args: Function args
        **kwargs: Function kwargs

    Returns: Decorated function exec result

    """
    try:
        result = function(self, *args, **kwargs)
        self.session.commit()
        return result
    except Exception as e:
        self.session.rollback()
        raise e


class BaseInterface:
    """
    An interface that guarantees the implementation of basic object management methods.
    Note:
    """

    def __new__(cls, *args, **kwargs):
        if cls is BaseInterface:
            raise TypeError("TypeError: Can't instantiate abstract class {name} directly".format(name=cls.__name__))
        return object.__new__(cls)

    @abc.abstractmethod
    def create(self, entity: Type[AbcDBModel]) -> None: raise NotImplementedError

    @abc.abstractmethod
    def read_all(self, model: AbcDBModel = AbcDBModel, *, limit=1000) -> List[Optional[Type[AbcDBModel]]]: raise NotImplementedError

    @abc.abstractmethod
    def read_by(self, where, model: AbcDBModel = AbcDBModel, *, limit=1000) -> List[Optional[Type[AbcDBModel]]]: raise NotImplementedError

    @abc.abstractmethod
    def read_in_batches(self, model: AbcDBModel = AbcDBModel, *, batch_size=1000) -> Generator[Type[AbcDBModel], None, None]: raise NotImplementedError

    @abc.abstractmethod
    def update_by(self, where: dict, values: dict, model: AbcDBModel = AbcDBModel) -> None: raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity: Type[AbcDBModel]) -> None: raise NotImplementedError

    @abc.abstractmethod
    def delete_all(self, model: AbcDBModel = AbcDBModel) -> None: raise NotImplementedError

    @abc.abstractmethod
    def delete_by(self, where: dict, model: AbcDBModel = AbcDBModel) -> None: raise NotImplementedError


class BaseDBController(BaseInterface, ABC):
    """
    Contains a basic set of private methods for performing operations with database objects.
    """

    def __init__(self, session: Session):
        """
        Args:
            session: Session object for executing commands in the database (transport layer)
        """
        self.__session = session

    @property
    def session(self):
        return self.__session.session

    @debug
    @commit
    def _create(self, entity: Type[AbcDBModel]) -> None:
        self.session.add(entity)

    @debug
    def _read_all(self, model: AbcDBModel, *, limit=1000) -> List[Optional[AbcDBModel]]:
        return self.session.query(model).limit(limit).all()

    @debug
    def _read_by(self, where, model: AbcDBModel, *, limit=1000) -> List[Optional[AbcDBModel]]:
        return self.session.query(model).filter_by(**where).limit(limit).all()

    @debug
    def _read_in_batches(self, model: AbcDBModel, *, batch_size=100) -> Generator[AbcDBModel, None, None]:
        for r in self.session.query(model).yield_per(batch_size):
            yield r

    @debug
    @commit
    def _update_by(self, model: AbcDBModel, where: dict, values: dict) -> None:
        self.session.query(model).filter_by(**where).update(values)

    @debug
    @commit
    def _delete(self, entity: Type[AbcDBModel]) -> None:
        self.session.delete(entity)

    @debug
    @commit
    def _delete_all(self, model: AbcDBModel) -> None:
        self.session.query(model).delete()

    @debug
    @commit
    def _delete_by(self, model: AbcDBModel, where: dict) -> None:
        self.session.query(model).filter_by(**where).delete()
