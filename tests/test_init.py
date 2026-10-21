# coding=UTF-8

"""
@file: __init__.py
测试包初始化导入模块
"""


# 导入
import pytest
import time, logging
import src.core.__init__ as it



@ pytest.fixture
def task_self():
    manager = it._ThreadManager
    log = logging.getLogger()
    setattr(manager, 'logger', log)
    return manager()



def test_thread(task_self):
    q = task_self.thread(1, '[PyAI]Test-Thread')
    test_func = lambda:time.sleep(5)
    for y_or_n in True,False:
        is_completed = task_self.add_task(q, test_func, ())
        assert y_or_n == is_completed



@ pytest.fixture
def test_existing_raise():
    p = it.PyAI
    setattr(p, 'is_existence', (False,))
    try:
        pyai = p()
    except SystemExit:
        pass
    else:
        raise AssertionError('The inited process is not run')