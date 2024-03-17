import inspect
import typing

from .path import PathHelper
from .time import TimeHelper
from .logging import LoggingHelper

_debug = False
_is_inited = False


class Helper:
    path: PathHelper
    time = TimeHelper()
    logging: LoggingHelper

    @classmethod
    def init(cls, log_path: str = 'data/log.txt', debug: bool = False):
        """在程序入口文件(main.py)开头调用此函数以初始化"""
        global _debug, _is_inited

        if _is_inited:
            return

        _debug = debug
        _is_inited = True

        frame = inspect.stack()[1]
        caller_file_path = frame.filename

        cls.path = PathHelper(caller_file_path)
        cls.logging = LoggingHelper(log_path, cls.path.working_dir)

    @staticmethod
    def safe(func: typing.Callable, *args, _handle=BaseException, _default: any = None,
             **kwargs) -> any:
        """
        用于安全地调用其他函数，并在调用过程中捕获指定类型的异常，以便程序能够继续执行，而不会因为异常而中断。

        :param func: 要调用的函数
        :param _handle: 要捕获的异常类型，默认为 BaseException
        :param _default: 当异常发生时要返回的默认值，默认值为 None。
        :return:
        """
        try:
            return func(*args, **kwargs)
        except _handle as e:
            if not _debug:
                return _default
            raise e

