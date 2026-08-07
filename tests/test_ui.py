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
    cmds = {
        'home':{
            'chat':test_function
        }
    }
    self = ui.Ui(**cmds)
    return self


def test_built_ui(get_self):
    get_self.build_ui()