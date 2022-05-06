from sqlalchemy.ext.declarative import declarative_base


class ReprExtension:
    """
    Representation extensions for the base alchemy class
    """
    @property
    def to_dict(self) -> dict:
        return self.__items_to_dict()

    @property
    def to_values(self) -> list:
        return self.__items_to_values_list()

    @property
    def to_str(self) -> str:
        return self.__to_str()

    def __to_str(self) -> str:
        return ":".join([self.__class__.__name__, str(self.__items_to_dict())])

    def __items_to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __items_to_values_list(self):
        return [f"{k} = {v}" for k, v in self.__dict__.items() if not k.startswith("_")]


BaseModel = declarative_base(cls=ReprExtension)
