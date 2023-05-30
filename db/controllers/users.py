from typing import NoReturn

from db.controllers.base import BaseDBController
from db.entities.users import UsersEntity

class UsersController(BaseDBController[UsersEntity]):

    def delete_all(self) -> NoReturn:
        """
        Deletes all users from table.
        :return: NoReturn
        """
        with self.transport.session_manager() as session:
            session.query(self.model).delete()
            session.commit()