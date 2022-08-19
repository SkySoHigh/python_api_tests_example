from api.controllers.db import BaseDBController
from models.db import ExampleTable


class ExampleDBController(BaseDBController[ExampleTable]):
    pass
