# coding=UTF-8

"""
@file: voice.py
"""

# 模块导入
import json
import winsound
import edge_tts as tts

__all__ = [
    'init',
    'Voice'
]



# 获取日志记录器
global logger
def init(get_logger) -> None:
    """
    初始化模块
    :param get_logger: 获取记录器的调用方法
    :return: None
    """
    global logger
    logger = get_logger(__name__)




class Voice:
    """
    语音合成
    """
    with open('config.json', 'r', encoding='UTF-8') as f:
        config = json.load(f)['voice_config']
        cache_path = config['cache_path']



    def __init__(self, voice:str, timeout:int) -> None:
        """
        Initiate voice
        """
        self.logger = logger
        self.v = voice
        self.timeout = timeout
        self.logger.debug(f'{voice}, {timeout}')
        self.logger.info('Init voice')



    def _request_tts(self, text:str) -> None:
        """
        向 TTS 服务请求获取人声文件
        :param text: 转换文本
        :return: None
        """
        self.logger.debug(text)
        response = tts.Communicate(text, self.v,
                                   connect_timeout=self.timeout, receive_timeout=self.timeout)
        response.save(self.cache_path)
        self.logger.info('Request to the TTS')



    def _play(self) -> None:
        """
        播放保存的音频
        :return: None
        """
        winsound.PlaySound(self.cache_path, winsound.SND_FILENAME)
        self.logger.info('Play the audio')



    def say(self, text:str) -> None:
        """
        下载并播放音频
        :param text: 转换文本
        :return: None
        """
        self.logger.info('Say')
        self.logger.debug(text)
        self._request_tts(text)
        self._play()