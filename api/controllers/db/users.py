from typing import Type, List, Optional, Generator

from api.controllers.db import BaseDBController, default_all
from models.db import UserExample


@default_all
class UserExampleDBController(BaseDBController):

    def create(self, entity: Type[UserExample]) -> None:
        pass

    def read_all(self, model: UserExample = UserExample, *, limit=1000) -> List[Optional[Type[UserExample]]]:
        pass

    def read_by(self, where, model: UserExample = UserExample, *, limit=1000) -> List[Optional[Type[UserExample]]]:
        pass

    def read_in_batches(self, model: UserExample = UserExample, *, batch_size=1000) -> Generator[Type[UserExample], None, None]:
        pass

    def update_by(self, where: dict, values: dict, model: UserExample = UserExample) -> None:
        pass

    def delete(self, entity: Type[UserExample]) -> None:
        pass

    def delete_all(self, model: UserExample = UserExample) -> None:
        pass

    def delete_by(self, where: dict, model: UserExample = UserExample) -> None:
        pass
