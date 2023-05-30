# -*- coding: utf-8 -*-
from typing import TypeVar

from pydantic import BaseModel

ReqSchema = TypeVar('ReqSchema')
RespSchema = TypeVar('RespSchema')


class BaseSchema(BaseModel):
    ...
