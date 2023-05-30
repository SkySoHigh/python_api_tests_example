# -*- coding: utf-8 -*-
"""The module users schema objects builders with"""

from api.schemas.user_schema import UsersSchema, GenderEnum
from core.random_generator import get_random_generator

rand_gen = get_random_generator()


class UserSchemaBuilder:

    @staticmethod
    def build_random():
        return UsersSchema(
            mail=rand_gen.person.email(domains=['example.ru']),
            password=rand_gen.person.password(30, hashed=True),
            gender=rand_gen.random.choice([GenderEnum.MALE.value, GenderEnum.FEMALE.value]),
            name=rand_gen.person.name(),
            check11=True,
            check12=False,
            check21=True,
            check22=bool(rand_gen.random.getrandbits(1)),
            check23=bool(rand_gen.random.getrandbits(1)))
