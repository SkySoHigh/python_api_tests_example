from api.schemas.user_schema import UsersSchema, GenderEnum
from db.entities.users import UsersEntity


class UsersConverters:
    @staticmethod
    def entity_to_schema(entity: UsersEntity) -> UsersSchema:
        return UsersSchema(id=entity.id,
                           password=entity.password,
                           name=entity.name,
                           mail=entity.mail,
                           gender=GenderEnum.MALE if entity.gender==0 else GenderEnum.FEMALE,
                           check11=entity.check11,
                           check12=entity.check12,
                           check21=entity.check21,
                           check22=entity.check22,
                           check23=entity.check23
                           )
