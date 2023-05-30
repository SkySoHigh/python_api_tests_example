# -*- coding: utf-8 -*-
from enum import Enum
from typing import List, Optional

from api.schemas.base import BaseSchema


class GenderEnum(str, Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class UsersSchema(BaseSchema):
    id: Optional[int]
    mail: str
    password: str
    name: str
    gender: GenderEnum
    check11: bool
    check12: bool
    check21: bool
    check22: bool
    check23: bool
    vars: Optional[List[str]]

    class Config:
        use_enum_values = True

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.dict(exclude={'vars', 'id'}) == other.dict(exclude={'vars', 'id'})
        return NotImplemented


class UserSchemaResponse(BaseSchema):
    state: str
    user: Optional[UsersSchema]
