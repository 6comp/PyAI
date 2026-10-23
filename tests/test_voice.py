# coding = UTF-8

"""
@file: test_voice.py
测试声音模块
"""


# 导入
import logging
import pytest
from src.core import voice



@pytest.fixture
def voice_self():
    def log(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - {%(lineno)d}')
        stream = logging.StreamHandler()
        stream.setLevel(logging.DEBUG)
        stream.setFormatter(formatter)
        logger.addHandler(stream)
        return logger
    voice.init(log)

    class TestTTS:
        def __init__(self, *args, **kwargs):pass
        def save_sync(self, path:str):pass
    class TestPlayer:
        def __init__(self, path:str):pass
        def play(self):pass
        def stop(self):pass
        def close(self):pass
    v = voice.Voice
    setattr(v, 'config', {'voice_config':{'cache_path':'TESTING PATH'}})
    setattr(voice.tts, 'Communicate', TestTTS)
    setattr(voice.player, 'Playback', TestPlayer)
    v = v();v.voice_choice = 'TEST MODULE'
    return v



def test_sa_st(voice_self):
    """
    测试说话功能
    :param voice_self: 类对象
    :return: None
    """
    content = 'TESTING CONTENT'
    for _ in range(5):
        voice_self.say(content)
    assert len(voice_self.player_self) == 5
    voice_self.stop()
    assert len(voice_self.player_self) == 0