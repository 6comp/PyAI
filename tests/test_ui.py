# coding = UTF-8


import logging
import pytest
from tkinter import messagebox
from core import ui

@ pytest.fixture()
def get_self():
    def _return(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - {%(lineno)d}')
        stream = logging.StreamHandler()
        stream.setLevel(logging.DEBUG)
        stream.setFormatter(formatter)
        logger.addHandler(stream)
        return logger
    ui.init(_return)

    def test_function(*args, **kwargs):
        print(args, kwargs)
        return 1234567890
    cmds = {
        'chat':test_function,
        'get_api':test_function,
        'set_api':test_function,
        'get_setting':test_function
    }
    self = ui.Ui(**cmds)
    return self


def test_built_ui(get_self):
    get_self.build_ui()