# -*- coding: utf-8 -*-
from collections.abc import Iterable
from typing import List
from typing import Protocol, Optional

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapper
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.orm.interfaces import MapperProperty

from libs.utils import classproperty

Base = declarative_base()


class MappingProtocol(Protocol):
    __mapper__: Mapper


class InspectionMixin(Base):
    """ Mixin to with model/object inspection methods
    """
    __abstract__ = True

    @classproperty
    def primary_keys(cls: MappingProtocol) -> List[MapperProperty]:
        mapper = cls.__mapper__
        return [mapper.get_property_by_column(column) for column in mapper.primary_key]

    @classproperty
    def columns(cls) -> List[str]:
        return inspect(cls).columns.keys()

    @classproperty
    def relations(cls: MappingProtocol) -> List[str]:
        return [c.key for c in cls.__mapper__.iterate_properties if isinstance(c, RelationshipProperty)]

    @classproperty
    def hybrid_properties(cls) -> List[str]:
        items = inspect(cls).all_orm_descriptors
        return [item.__name__ for item in items if isinstance(item, hybrid_property)]


class SerializeMixin(InspectionMixin):
    """Mixin to make model serializable"""

    __abstract__ = True

    def to_dict(self, nested: bool = False, hybrid_attributes: bool = False,
                exclude: Optional[List[str]] = None) -> dict:
        """
        Converts db object to dict (supports nested objects)
        Args:
            nested:  flag to return nested relationships' data if true
            hybrid_attributes: flag to include hybrid attributes if true
            exclude:
        """
        result = dict()

        if exclude is None:
            view_cols = self.columns
        else:
            view_cols = filter(lambda e: e not in exclude, self.columns)

        for key in view_cols:
            result[key] = getattr(self, key)

        if hybrid_attributes:
            for key in self.hybrid_properties:
                result[key] = getattr(self, key)

        if nested:
            for key in self.relations:
                obj = getattr(self, key)

                if isinstance(obj, SerializeMixin):
                    result[key] = obj.to_dict(hybrid_attributes=hybrid_attributes)
                elif isinstance(obj, Iterable):
                    result[key] = [
                        o.to_dict(hybrid_attributes=hybrid_attributes) for o in obj
                        if isinstance(o, SerializeMixin)
                    ]
        return result
