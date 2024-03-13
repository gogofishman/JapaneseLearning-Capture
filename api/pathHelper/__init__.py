import os
import pathlib
import sys


class PathHelper:

    def __init__(self):
        self.working_dir = None
        self.data_dir = pathlib.Path(getattr(sys, '_MEIPASS', os.getcwd()))
        """程序打包后的内部缓存目录（比如：AppData/Local/Temp ）"""

    def init(self, main_path: str):
        self.working_dir = pathlib.Path(sys.executable if getattr(sys, 'frozen', False) else main_path).parent
        """工作目录（执行文件所在目录）"""

    @staticmethod
    def Path(path: str):
        """返回一个Path对象"""
        return pathlib.Path(path)

    @staticmethod
    def get_file_dir(file_path: str):
        """获取当前文件所在目录\n\n这样用：get_file_dir(__file__)"""
        return pathlib.Path(sys.executable if getattr(sys, 'frozen', False) else file_path).parent


path_helper = PathHelper()
