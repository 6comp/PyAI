# coding=UTF-8

import pytest
import logging
from core import datamanage


# @ pytest.fixture
def test_get_self():
    def _return(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler())
        return logger
    datamanage.init(_return)
    manager = datamanage.DataManager()
    return manager