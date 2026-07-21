# coding=UTF-8

# 导入
import pytest
import logging
import sqlite3
import keyring
from core import datamanage



@ pytest.fixture
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
    datamanage.init(_return)
    manager = datamanage.DataManager()
    return manager


def test_save_dialogs(get_self):
    get_self.save_dialogs(('a','A','0000.0.0'),('b','B','0000.0.0'))
    with sqlite3.connect('data\\dialogs.db') as conn:
        cursor = conn.cursor()
        end_index = cursor.execute('SELECT id FROM dialogs').fetchall()[-1][0]
        result = cursor.execute('SELECT * FROM dialogs WHERE id=?',(end_index,)).fetchone()
        assert result


def test_save_info(get_self):
    get_self.save_info('聪明人，但不聪明','傻子，纯傻子')
    with sqlite3.connect('data\\dialogs.db') as conn:
        cursor = conn.cursor()
        index = cursor.execute('SELECT id FROM info').fetchall()[-1]
    assert cursor.execute('select * from info WHERE id=?',(index[0],)).fetchone()


def test__get_aeskey(get_self):
    assert get_self._get_aeskey()
    with sqlite3.connect('data\\settings.db') as conn:
        cursor = conn.cursor()
        secret_data = cursor.execute('SELECT * FROM secret WHERE key=?',('API-KEY',)).fetchone()
        secret_iv = cursor.execute('SELECT * FROM secret WHERE key=?',('AES-IV',)).fetchone()
        assert secret_data, secret_iv


def test__destroyed_secret(get_self):
    get_self._destroyed_secret()
    assert keyring.get_password(datamanage.NAME, datamanage.AES_API) is None
    with sqlite3.connect('data\\settings.db') as conn:
        cursor = conn.cursor()
        assert not cursor.execute('SELECT * FROM secret').fetchall()


def test_set_api(get_self):
    get_self.set_api('原神牛逼666')
    with sqlite3.connect('data\\settings.db') as conn:
        cursor = conn.cursor()
        secret = cursor.execute('SELECT * FROM secret WHERE key=?',('API-KEY',)).fetchone()
        assert secret


def test_get_api(get_self):
    api = get_self.get_api()
    assert api