# coding=UTF-8

"""
@file: voice.py
"""


# 模块导入
import edge_tts as tts
import just_playback as player


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

    def __init__(self, timeout:int=15) -> None:
        """
        Initiate voice
        """

        config = self.config['voice_config']
        self.cache_path = config['cache_path']

        self.voice_logger = voice_logger
        self.voice_choice = None
        self.timeout = timeout
        self.player_self:list[player.Playback] = []
        self.voice_logger.debug(f'{self.voice_choice}, {timeout}')
        self.voice_logger.info('Initiate have down (voice)')



    def _rs_tts(self, text:str) -> None:
        """
        向 TTS 服务请求获取人声文件
        :param text: 转换文本
        :return: None
        """
        if not self.voice_choice is None:
            self.voice_logger.debug(text)
            try:
                response = tts.Communicate(text, self.voice_choice,
                                           connect_timeout=self.timeout, receive_timeout=self.timeout)
                response.save_sync(self.cache_path)
            except Exception as e:
                self.voice_logger.error(f'TTS error :{e}')
        self.voice_logger.warning('The voice choice is None')
        self.voice_logger.info('Requested to the TTS')



    def _play(self) -> None:
        """
        播放保存的音频
        :return: None
        """
        p = player.Playback(self.cache_path)
        p.play()
        self.player_self.append(p)
        self.voice_logger.info('Play the audio')



    def stop(self) -> None:
        """
        停止正在播放的音频
        :return: None
        """
        for p in self.player_self:
            p.stop(); p.close()
        self.player_self.clear()
        self.voice_logger.info('Stopped all playing event')



    def say(self, text:str) -> None:
        """
        下载并播放音频
        :param text: 转换文本
        :return: None
        """
        self.voice_logger.debug(text)
        self._rs_tts(text)
        self._play()
        self.voice_logger.info('Saied content')