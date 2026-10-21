# coding=UTF-8

"""
@file: test_api.py
测试 api 模块
"""

# 导入
import logging
import pytest
from src.core import api



@ pytest.fixture
def self():
    def log(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - {%(lineno)d}')
        stream = logging.StreamHandler()
        stream.setLevel(logging.DEBUG)
        stream.setFormatter(formatter)
        logger.addHandler(stream)
        return logger
    api.init(log)

    s = api.Api
    class test_post:
        def __init__(self, *args, **kwargs):
            self.encoding = 'UTF-8'
            self.status_code = 200
            self.headers = {'EXAMPLE-HEADER':'EXAMPLE HEADER CONTENT'}
            self.cookies = 'TESTING COOKIES CONTENT'
            self.text = '''{"choices":
                             [
                                 {
                                     "finish_reason":"stop",
                                     "message":{"content":"THIS IS A PIECE OF CONTENT"}
                                  }
                             ]
                         }'''
            self.ok = True
    setattr(api.requests, 'post', test_post)

    return s()



def test_chat(self):
    """
    测试交流功能
    :param self: 类对象
    :return: None
    """
    key, content, info = \
        'TEST API SECRET', 'TEST CONTENT', {"对话者相关属性":{"0":{"姓名":"TEST-NAME","性别":"MALE","性格":"EXAMPLE","补充":"EXAMPLE"},"1":{"姓名":"TEST-NAME","性别":"FEMALE","性格":"EXAMPLE","补充":"EXAMPLE"}},"相关记忆":['THIS IS THE FIRST EXAMPLE MEMORY', 'THIS IS A SECOND EXAMPLE MEMORY'],"正在进行的对话":{"0":"HELLO","1":"YOU FINE TOO"}}
    for func, arg in ((self.add_api, key), (self.add_info, info)):
        assert not self.chat(content)
        func(arg)
    assert self.chat(content)



def test_add_info(self):
    """
    测试添加信息功能
    :param self: 类对象
    :return: None
    """
    info = {"对话者相关属性":{"0":{"姓名":"TEST-NAME","性别":"MALE","性格":"EXAMPLE","补充":"EXAMPLE"},"1":{"姓名":"TEST-NAME","性别":"FEMALE","性格":"EXAMPLE","补充":"EXAMPLE"}},"相关记忆":['THIS IS THE FIRST EXAMPLE MEMORY', 'THIS IS A SECOND EXAMPLE MEMORY'],"正在进行的对话":{"0":"HELLO","1":"YOU FINE TOO"}}
    self.add_info(info)
    ai_about = info['对话者相关属性']['0']
    ai_name = ai_about['姓名']
    user_about = info['对话者相关属性']['1']
    user_name = user_about['姓名']
    ai_setting = f'''
名字：{ai_name}
相关属性：{ai_about}
TA的名字：{user_name}
TA的属性：{user_about}
相关记忆：{info['相关记忆']}
        '''
    message = self.get_messages()
    assert ai_setting == message[0]['content']
    assert message[1:] == [{'content':'HELLO', 'role':'assistant'},{'content':'YOU FINE TOO', 'role':'user'}]



def test_ana_dialogs(self):
    """
    测试分析方法
    :param self: 类对象
    :return: None
    """
    message = self.get_messages()
    analysis = self.analysis_dialog(('EXAMPLE CONTENT','EXAMPLE CONTENT', 'EXAMPLE DATE'))
    assert analysis[0] == 'THIS IS A PIECE OF CONTENT'
    assert message == self.get_messages()



def test_request_to(self):
    """
    测试请求方法
    :param self: 类对象
    :return: None
    """
    payload = 'THIS IS A EXAMPLE PAYLOAD'
    answer = self._request(payload)
    assert answer[0] == 'THIS IS A PIECE OF CONTENT'