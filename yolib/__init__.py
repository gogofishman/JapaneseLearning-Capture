import inspect

from .path import PathHelper
from .time import TimeHelper
from .logging import LoggingHelper


class Helper:
    path: PathHelper
    time = TimeHelper()
    logging: LoggingHelper

    @classmethod
    def init(cls, log_path: str = 'data/log.txt'):
        """在程序入口文件(main.py)开头调用此函数以初始化"""
        frame = inspect.stack()[1]
        caller_file_path = frame.filename

        cls.path = PathHelper(caller_file_path)
        cls.logging = LoggingHelper(log_path, cls.path.working_dir)
