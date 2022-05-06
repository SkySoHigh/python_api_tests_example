# -*- coding: utf-8 -*-
from typing import TypeVar
AbcDBModel = TypeVar("AbcDBModel")

from .base import BaseModel

from .users import User
from .roles import Roles
