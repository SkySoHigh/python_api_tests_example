import logging
import logging.handlers
from api.controllers.http import BaseHttpController
from api.transport.http import HttpResponse
from libs.logger import log_func_call


class ExampleController(BaseHttpController):

    @log_func_call
    def get_main_page(self) -> HttpResponse:
        logging.info("Some logging info from get_main_page")
        return self.transport.get(self.endpoint)
