import os
import pathlib
import sys
import inspect


class PathHelper:

    def __init__(self, main_path: str):
        self.working_dir = pathlib.Path(sys.executable if getattr(sys, 'frozen', False) else main_path).parent
        """工作目录（执行文件所在目录）\n\n这样用：init(__file__)"""
        self.data_dir = pathlib.Path(getattr(sys, '_MEIPASS', os.getcwd()))
        """程序打包后的内部缓存目录（比如：AppData/Local/Temp ）"""

    @staticmethod
    def newPath(path: str):
        """返回一个Path对象"""
        return pathlib.Path(path)

    @staticmethod
    def current_file_dir():
        """获取当前文件所在目录"""

        frame = inspect.stack()[1]
        caller_file_path = frame.filename

        return pathlib.Path(sys.executable if getattr(sys, 'frozen', False) else caller_file_path).parent

    @staticmethod
    def create_file(file_path: pathlib.Path | str):
        """新建一个文件，中间路径也会跟着创建。如果已存在则忽略"""

        if not isinstance(file_path, pathlib.Path):
            file_path = pathlib.Path(file_path)

        file_dir = file_path.parent

        file_dir.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
