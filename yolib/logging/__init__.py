import pathlib

from ..path import PathHelper
from ..time import TimeHelper


class LoggingHelper:

    def __init__(self, log_path, working_dir: pathlib.Path):
        # 检测并生成log文件
        self.file_path = working_dir.joinpath(log_path)
        PathHelper.create_file(self.file_path)

    def _write(self, text):
        with open(self.file_path, 'a') as file:
            file.write(f'{text}\n')

    def debug(self, text: str):
        """记录所有debug日志，面向开发者"""
        output = f"[{TimeHelper.now_format()}] [DEBUG] {text}"
        print(output)

        self._write(output)

    def log(self, text: str):
        """用于记录刮削正常日志，面向用户"""
        output = f"[{TimeHelper.now_format()}] [LOG] {text}"
        print(output)

        self._write(output)

    def warning(self, text: str):
        """用于记录刮削警告日志，面向用户"""
        output = f"[{TimeHelper.now_format()}] [WARNING] {text}"
        print(output)

        self._write(output)

    def error(self, text: str):
        """用于记录刮削错误日志，面向用户"""
        output = f"[{TimeHelper.now_format()}] [ERROR] {text}"
        print(output)

        self._write(output)