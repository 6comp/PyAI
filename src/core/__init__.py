# coding=UTF-8



# 导入所有模块
import os
import json
import queue
import logging
import threading as th
import multiprocessing as mult
from . import api, datamanage, voice, ui

__all__ = [
    'main'
]



class PyAI:
    """
    PyAI
    """
    # 加载初始化文件
    with open(r'config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        log_config = config['log']

    # 文件夹创建
    if not all((
             os.path.exists('log'),
             os.path.exists('data')
             )):
        for folder in ('log','data'):
            os.mkdir(folder)



    def __init__(self) -> None:
        """
        PyAI Initialize
        """
        self.logger = self.get_logger(__name__)
        self.logger.debug(self.config)

        # 模块初始化
        api.init(self.get_logger)
        datamanage.init(self.get_logger)
        voice.init(self.get_logger)

        # 进程初始化
        self.q_p = mult.Queue(3)
        child_process = mult.Process(name='[PyAI]child-process',
                                     target=self._child_process, args=(self.q_p,),
                                     daemon=True)
        child_process.start()


        self.logger.info('Init PyAI')



    def _child_process(self, logger:logging.Logger, q:mult.Queue) -> None:
        """
        子线程，处理 I/O 的进程
        :param q: 队列对象
        :return: None
        """
        while True:
            logger.debug('Waiting a task')
            cmd = q.get()
            logger.debug(cmd)

            name, func, args = cmd['name'], cmd['function'], cmd['args']
            logger.debug(':'.join((name,func,args)))

            thread = th.Thread(name=name,
                               target=func,args=args,
                               daemon=True)
            thread.start()

            logger.info(f'{name} has started')



    def _play_voice(self, logger:logging.Logger, q:queue.Queue,
                    v:voice.Voice) -> None:
        """
        音频线程，接受音频播放指令
        :param q: 队列对象
        :return: None
        """
        while True:
            text = q.get()
            logger.info(f'say {text}')
            v.say(text)



    def PyAI(self) -> None:
        """
        PyAI 运行
        :return: None
        """



    def get_logger(self, name: str) -> logging.Logger:
        """
        获取日志记录器
        :param name: 记录器名
        :return: Logger
        """
        level = logging.DEBUG
        logger = logging.getLogger(name)
        logger.setLevel(level)

        formatter = logging.Formatter(self.log_config['format'])

        file_handler = logging.FileHandler(f'{self.log_config['dir']}{name}.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(level)
        logger.addHandler(stream_handler)

        return logger





def main() -> None:
    PyAI().PyAI()