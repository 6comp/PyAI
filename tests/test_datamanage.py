# coding=UTF-8

"""
@file: test_datamanage.py
测试 datamanage 模块
"""


# 导入
import pytest
import logging
from src.core import datamanage



@ pytest.fixture
def manager(tmp_path):
    def _return(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - {%(lineno)d}')
        stream = logging.StreamHandler()
        stream.setLevel(logging.DEBUG)
        stream.setFormatter(formatter)
        logger.addHandler(stream)
        return logger
    datamanage.init(_return)

    manager = datamanage.DataManager
    path = {
        'dialog':fr'{tmp_path}\dialogs.db',
        'system':fr'{tmp_path}\system.db',
        'setting':fr'{tmp_path}\settings.db'
            }
    setattr(manager, 'config', {'db_config':{'path':path}})
    class test_keyring:                                     # 用于测试的伪 keyring 模块
        keyring:dict = {}
        @classmethod
        def set_password(cls, username='', key='', value=''):cls.keyring[key] = value
        @classmethod
        def get_password(cls, service='', key=''):
            if key not in cls.keyring:return None
            return cls.keyring[key]
        @classmethod
        def delete_password(cls, service='', key=''):del cls.keyring[key]
    setattr(datamanage, 'keyring', test_keyring)

    return manager()



def test_sg_dialogs(manager):
    """
    测试保存和获取对话记录方法
    :param manager: 类对象
    :return: None
    """
    test_dialogs = ('test-name1','Hello!','1949.10.1'),('test-name2', 'Hi! It is a good day!', '1949.10.1')
    manager.save_dialogs(*test_dialogs)
    generator = manager.get_dialogs()
    assert tuple(generator) == test_dialogs[-1::-1]



def test_sg_info(manager):
    """
    测试保存和获取相关信息
    :param manager: 类对象
    :return: None
    """
    info = "THIS IS A TESTING CONTENT"
    manager.save_info(info)
    assert manager.get_info() == info
    assert manager.get_info(0) == info



def test_sg_api(manager):
    """
    测试保存获取密钥
    :param manager: 类对象
    :return: None
    """
    api = 'THIS IS A TESTING SECRET'
    manager.set_api(api)
    assert manager.get_api() == api



def test_ug_setting(manager):
    """
    测试更新获取设置
    :param manager: 类对象
    :return: None
    """
    setting = name, value = 'TEST-NAME', 'TEST-VALUE'
    for _ in range(2):
        manager.update_setting(*setting, False)
        manager.update_setting(*setting, True)
        assert manager.get_setting(name) == value
        assert manager.get_setting(name, True) == value



def test_destroyed(manager):
    manager.destroyed('all')
    assert not tuple(manager.get_dialogs())
    assert not manager.get_info()
    assert not manager.get_api()
    assert not manager.get_setting('TEST-NAME')