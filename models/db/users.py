# -*- coding: utf-8 -*-
from sqlalchemy import Boolean, Column, Integer, String, text

from models.db import BaseModel as Base

metadata = Base.metadata


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    deleted = Column(Boolean, nullable=False, server_default=text("false"))
