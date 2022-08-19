# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Sequence

from models.db import BaseModel as Base

class ExampleTable(Base):
    __tablename__ = 'example_table'
    id = Column(Integer, Sequence('example_id_seq'), primary_key=True)
    title = Column(String(64), nullable=False, unique=False)
    description = Column(String(64), nullable=False)
    number = Column(Integer, nullable=False)
