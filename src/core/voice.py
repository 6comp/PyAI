# coding=UTF-8

"""
@file: voice.py
"""

# 模块导入
import edge_tts as tts

__all__ = [
    'init',
    'Voice'
]



# 获取日志记录器
global voice_logger
def init(get_logger) -> None:
    """
    初始化模块
    :param get_logger: 获取记录器的调用方法
    :return: None
    """
    global voice_logger
    voice_logger = get_logger('voice')




class Voice:
    """
    语音合成
    """

    def __init__(self, voice:str, timeout:int=15) -> None:
        """
        Initiate voice
        """

        config = self.config['voice_config']
        self.cache_path = config['cache_path']

        self.logger = voice_logger
        self.v = voice
        self.timeout = timeout
        self.logger.debug(f'{voice}, {timeout}')
        self.logger.info('Initiate have down (voice)')



    def _request_tts(self, text:str) -> None:
        """
        向 TTS 服务请求获取人声文件
        :param text: 转换文本
        :return: None
        """
        self.logger.debug(text)
        response = tts.Communicate(text, self.v,
                                   connect_timeout=self.timeout, receive_timeout=self.timeout)
        response.save_sync(self.cache_path)
        self.logger.info('Request to the TTS')



    def _play(self) -> None:
        """
        播放保存的音频
        :return: None
        """
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