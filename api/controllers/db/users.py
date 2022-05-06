from typing import Type, List, Optional, Generator

from api.controllers.db import BaseDBController, default, default_all
from models.db import User, User


@default_all
class UserDBController(BaseDBController):

    def create(self, entity: Type[User]) -> None:
        pass

    def read_all(self, model: User = User, *, limit=1000) -> List[Optional[User]]:
        pass

    def read_by(self, where, model: User = User, *, limit=1000) -> List[Optional[User]]:
        pass

    def read_in_batches(self, model: User = User, *, batch_size=1000) -> Generator[User, None, None]:
        pass

    def update_by(self, where: dict, values: dict, model: User = User) -> None:
        pass

    def delete(self, entity: Type[User]) -> None:
        pass

    def delete_all(self, model: User = User) -> None:
        pass

    def delete_by(self, where: dict, model: User = User) -> None:
        pass
