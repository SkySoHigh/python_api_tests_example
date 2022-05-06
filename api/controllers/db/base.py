# -*- coding: utf-8 -*-
import abc
from abc import ABC
from typing import List, Optional, Type, Generator

from decorator import decorator

from api.transport import DBSession
from models.db import AbcDBModel


@decorator
def default(func, name: str = None, *args, **kwargs):
    """
    Method to decorate BaseDBController function with signature and typehints from interface.
    Mapping of functions occurs by the same name with the prefix "_".
    Example: Interface.create() -> BaseDBController._create().

    Args:
        func: Decorated function
        name: Name of the function in the BaseDBController. If empty: '_' + func.__name__  will be used.
        *args: Decorated function args (declared in the interface)
        **kwargs: Decorated function kwargs (declared in the interface)

    Returns: Original function from BaseDBController decorated with interface signature and typehints
    """

    try:
        name = name if name else f'_{func.__name__}'
        print(name)
        self, args = args[0], args[1::]
        def_func = getattr(self, str(name))
        return def_func(*args, **kwargs)
    except AttributeError:
        raise AttributeError(f'There is no default implementation with name: {name} '
                             f'among BaseDBController methods')


def default_all(cls):
    """
    Decorates all class method with default decorator.
    Warning: If there is default decorator on a method and default_all on a class, then only the latter will have an effect.

    Returns: NoReturn
    """
    for attr in cls.__dict__:
        if callable(getattr(cls, attr)) and not attr.startswith("_"):
            setattr(cls, attr, default(getattr(cls, attr)))
    return cls


@decorator
def trace(f, *args, **kw):
    kwstr = ', '.join('%r: %r' % (k, kw[k]) for k in sorted(kw))
    print("Calling %s with args %s, {%s}" % (f.__name__, args, kwstr))
    return f(*args, **kw)


@decorator
def commit(function, self, *args, **kwargs):
    try:
        result = function(self, *args, **kwargs)
        self.session.commit()
        return result
    except Exception as e:
        self.session.rollback()
        raise e


class BaseInterface:

    def __new__(cls, *args, **kwargs):
        if cls is BaseInterface:
            raise TypeError("TypeError: Can't instantiate abstract class {name} directly".format(name=cls.__name__))
        return object.__new__(cls)

    @abc.abstractmethod
    def create(self, entity: Type[AbcDBModel]) -> None: raise NotImplementedError

    @abc.abstractmethod
    def read_all(self, model: AbcDBModel = AbcDBModel, *, limit=1000) -> List[
        Optional[AbcDBModel]]: raise NotImplementedError

    @abc.abstractmethod
    def read_by(self, where, model: AbcDBModel = AbcDBModel, *, limit=1000) -> List[
        Optional[AbcDBModel]]: raise NotImplementedError

    @abc.abstractmethod
    def read_in_batches(self, model: AbcDBModel = AbcDBModel, *, batch_size=1000) -> Generator[
        AbcDBModel, None, None]: raise NotImplementedError

    @abc.abstractmethod
    def update_by(self, where: dict, values: dict, model: AbcDBModel = AbcDBModel) -> None: raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity: Type[AbcDBModel]) -> None: raise NotImplementedError

    @abc.abstractmethod
    def delete_all(self, model: AbcDBModel = AbcDBModel) -> None: raise NotImplementedError

    @abc.abstractmethod
    def delete_by(self, where: dict, model: AbcDBModel = AbcDBModel) -> None: raise NotImplementedError


class BaseDBController(BaseInterface, ABC):

    def __init__(self, session: DBSession):
        """
        Args:
            session: Session object for executing commands in the database (transport layer)
        """
        self.__session = session

    @property
    def session(self):
        return self.__session.session

    @trace
    @commit
    def _create(self, entity: Type[AbcDBModel]) -> None:
        self.session.add(entity)

    @trace
    def _read_all(self, model: AbcDBModel, *, limit=1000) -> List[Optional[AbcDBModel]]:
        return self.session.query(model).limit(limit).all()

    @trace
    def _read_by(self, where, model: AbcDBModel, *, limit=1000) -> List[Optional[AbcDBModel]]:
        return self.session.query(model).filter_by(**where).limit(limit).all()

    @trace
    def _read_in_batches(self, model: AbcDBModel, *, batch_size=100) -> Generator[AbcDBModel, None, None]:
        for r in self.session.query(model).yield_per(batch_size):
            yield r

    @trace
    @commit
    def _update_by(self, model: AbcDBModel, where: dict, values: dict) -> None:
        self.session.query(model).filter_by(**where).update(values)

    @trace
    @commit
    def _delete(self, entity: Type[AbcDBModel]) -> None:
        self.session.delete(entity)

    @trace
    @commit
    def _delete_all(self, model: AbcDBModel) -> None:
        self.session.query(model).delete()

    @trace
    @commit
    def _delete_by(self, model: AbcDBModel, where: dict) -> None:
        self.session.query(model).filter_by(**where).delete()
