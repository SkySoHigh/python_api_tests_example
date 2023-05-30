# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean

from db.entities.base import BaseModel


class UsersEntity(BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    check11 = Column(Boolean)
    check12 = Column(Boolean)
    check21 = Column(Boolean)
    check22 = Column(Boolean)
    check23 = Column(Boolean)
    gender = Column(Integer)
    mail = Column(String(50))
    name = Column(String(50))
    password = Column(String(255))
