from sqlalchemy import MetaData

from .mixins import SerializeMixin


class BaseModel(SerializeMixin):
    """ Abstract declarative base model with mixins
    More info: https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#abstract
    """
    __abstract__ = True
    metadata = MetaData()
