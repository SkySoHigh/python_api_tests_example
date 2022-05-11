# -*- coding: utf-8 -*-
from sqlalchemy import Boolean, Column, Integer, String, text, Sequence

from models.db import BaseModel as Base


class UserExample(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    username = Column(String(64), nullable=False, unique=False)
    password = Column(String(64), nullable=False)
    deleted = Column(Boolean, nullable=False, server_default=text("false"))
