# coding=UTF-8

"""
@file: test_api.py
测试 api 模块
"""



# 测试导入
import os
import dotenv
import src.core.api as api



dotenv.load_dotenv('.env.local')


def test_api_request():
    test_key = os.getenv("APIKYE")
    if test_key is None:
        raise Exception("API key not set")
    test_msg = [{'content':'你是一个 ai 智能助手', 'role':'system'}]
    api_self = api.Api(test_msg, test_key)
    assert api_self.request('你好啊') is not None
