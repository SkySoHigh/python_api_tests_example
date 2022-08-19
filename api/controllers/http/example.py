import logging
import logging.handlers

from api.controllers.http import BaseHttpController
from api.transport.http import HttpResponse
from libs.logger import log_func_call
from models.http import ExampleModel


class ExampleController(BaseHttpController):

    @log_func_call
    def create_example(self, model: ExampleModel) -> HttpResponse:
        return self.transport.post(self.endpoint, data=model.json())
