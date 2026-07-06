# coding=UTF-8

"""
@file: test_api.py
测试 api 模块
"""

# 测试导入
import os
import logging
import dotenv
import pytest
import src.core.api as api


dotenv.load_dotenv('.env.local')


@ pytest.fixture
def logger():
    def _return(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler())
        return logger
    return _return


@ pytest.fixture(autouse=True)
def api_self(logger):
    test_key = os.getenv("APIKYE")
    if test_key is None:
        raise Exception("API key not set")
    api.init(logger)
    test_msg = [{'content':'你是一个 ai 智能助手', 'role':'system'}]
    return api.Api(test_msg, test_key)


def test_api_chat(api_self):
    assert api_self.chat('你好啊') is not None


def test_api_analysis_dialog(api_self):
    assert api_self.analysis_dialog(('借钱王','111 兄弟可有碎银几两', '2026.1.1'),('铜钱捞石','滚滚滚！', '2026.1.1')) is not None