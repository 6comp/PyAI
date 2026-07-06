# coding=UTF-8

"""
@file: datamanage.py
"""

# 模块导入
import json
import sqlite3
import secrets
import base64
import hmac
import hashlib

__all__ = [
    'DataManager',
    'init'
]



# 获取日志记录器
global logger
def init(get_logger) -> None:
    """
    初始化模块
    :param get_logger: 获取记录器调用方法
    :return: None
    """
    global logger
    logger = get_logger(__name__)



class DataManager:
    """
    数据管理的封装
    """
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        db_paths:dict[str,str] = config['db_config']['path']



    def __init__(self) -> None:
        """
        Initiate data manager
        """
        self.logger = logger

    def save_dialog(self, *dialogs:tuple[str, str, str]) -> bool|None:
        """
        保存聊天记录
        :param dialogs: 聊天记录 ('a','111 兄弟可有碎银几两', '2026.1.1'),('b','滚蛋！', '2026.1.1')
        :return: bool|None
        """