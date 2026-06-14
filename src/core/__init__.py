# coding=UTF-8



# 导入所有模块
import json
import logging
from . import api, file, voice


class PyAI:
    """
    PyAI
    """
    # 加载初始化文件
    with open(r'config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        log_config = config['log']



    def __init__(self) -> None:
        """
        PyAI Init
        """
        self.logger = self.get_logger(__name__)
        api.init(self.get_logger)
        self.logger.info('Init PyAI')



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