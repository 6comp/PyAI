# coding=UTF-8



# 导入所需模块
import os
import json
import queue
import logging
import argparse
import typing as tp
import threading as th
from . import api, datamanage, voice, ui


__all__ = [
    'main'
]




class _ThreadManager:
    """
    线程管理器
    """
    #
    # def __init__(self) -> None:
    #     self.logger = None



    def _thread_processor(self, name: str, logger: logging.Logger, q: queue.Queue) -> None:
        """
        可调用对象处理器
        :param q: 队列对象
        :return: None
        """
        logger.info(f'Create a child thread: {name}')

        while True:
            cmd = q.get()
            target, args = cmd
            target(*args)
            logger.debug('Done')



    def thread(self, queue_max: int, thread_name: str = '[PyAI]Child-Thread', daemon: bool = True) -> queue.Queue:
        """
        创建线程函数（或方法）处理器
        返回一个队列对象
        :param queue_max: 队列最大大小
        :param thread_name: 线程名
        :param daemon: 是否启用守护线程
        :return: queue.Queue
        """
        self.logger.debug(f'QueueMaxSize: {queue_max} | ThreadName: {thread_name} | IsDaemon: {daemon}')

        q = queue.Queue(queue_max)
        t = th.Thread(name=thread_name,
                      target=self._thread_processor,
                      args=(thread_name, self.logger, q),
                      daemon=daemon)
        t.start()

        self.logger.info('Create ended')
        return q



    def add_task(self, q: queue.Queue, target: tp.Callable, args: tuple) -> bool:
        """
        向子线程添加任务
        :param q: 子线程的队列对象
        :param target: 可调用对象
        :param args: 传给可调用对象的参数
        :return: bool
        """
        if not q.full():
            q.put((target, args))
            self.logger.debug('Completed adding task')
        else:
            self.logger.warning('The Queue is Full')
            return False
        self.logger.info('Add task ended')
        return True




class PyAI(_ThreadManager, datamanage.DataManager, api.Api, ui.Ui, voice.Voice):
    """
    PyAI
    """
    path = os.path

    # 判断所需文件是否存在
    file_paths = ('analysis_config',
                  'config.json',
                  r'img\PyAIICO.ico',
                  r'img\PyAI-IMG(white).png',
                  r'img\PyAI-IMG(black)(normal).png',
                  r'img\PyAI-IMG(white)(normal).png',
                  r'docs\HelpIndex.html')
    is_existence = (path.isfile(p) for p in file_paths)
    if not is_existence:
        super().show_warn('error', '错误', '有所需文件缺失')
        raise SystemExit('Some required file are missing!')

    # 加载初始化文件
    with open(r'config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        log_config = config['log']

    # 文件夹创建
    if not all((
             path.exists('log'),
             path.exists('data')
             )):
        for folder in ('log','data'):
            os.mkdir(folder)



    def __init__(self) -> None:
        """
        PyAI Initialize
        """
        a_parse = argparse.ArgumentParser('PyAI')
        a_parse.add_argument('-d', '--debug', action='store_true')
        args = a_parse.parse_args()
        self.logger_level = logging.DEBUG if args.debug else logging.INFO

        self.logger = self.get_logger(__name__)
        self.logger.debug(self.config)

        # 模块初始化
        api.init(self.get_logger)
        datamanage.init(self.get_logger)
        ui.init(self.get_logger)
        voice.init(self.get_logger)
        super(_ThreadManager, self).__init__()
        super(datamanage.DataManager, self).__init__()
        super(api.Api, self).__init__()
        super(ui.Ui, self).__init__('zh-CN-XiaoyiNeural')


        self.logger.info('Init PyAI')



    def pyai(self) -> None:
        """
        PyAI 运行
        :return: None
        """
        ui.Ui.build_ui(self)
        self.logger.info('Building ui ended')



    def get_logger(self, name: str) -> logging.Logger:
        """
        获取日志记录器
        :param name: 记录器名
        :return: Logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(self.logger_level)

        formatter = logging.Formatter(self.log_config['format'])

        file_handler = logging.FileHandler(f'{self.log_config['dir']}{name}.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(self.logger_level)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(self.logger_level)
        logger.addHandler(stream_handler)

        return logger





def main() -> None:
    app = PyAI()
    app.pyai()