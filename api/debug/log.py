import os
from datetime import datetime


class Logging:

    def __init__(self):
        # 检测并生成data文件夹
        if os.path.exists('data') is False:
            os.mkdir('data')

    @staticmethod
    def _now() -> str:
        """获取当前时间，精确到毫秒，如（'2024-03-04 18:25:09.346'）"""
        time = datetime.now()
        microsecond = str(round(time.microsecond / 1000000, 3))[2:]

        zero_count = 3 - len(microsecond)
        microsecond = microsecond + "0" * zero_count

        return f"{time.strftime('%Y-%m-%d %H:%M:%S')}.{microsecond}"

    @staticmethod
    def _write(file_name, text):
        file_path = f'data\\{file_name}.txt'

        with open(file_path, 'a') as file:
            file.write(f'{text}\n')

    def debug(self, text: str):
        """记录所有debug日志，面向开发者"""
        output = f"[{self._now()}] [DEBUG] {text}"
        print(output)

        self._write('debug', output)

    def log(self, text: str):
        """用于记录刮削正常日志，面向用户"""
        output = f"[{self._now()}] [LOG] {text}"
        print(output)

        self._write('log', output)
        self._write('debug', output)

    def warning(self, text: str):
        """用于记录刮削警告日志，面向用户"""
        output = f"[{self._now()}] [WARNING] {text}"
        print(output)

        self._write('log', output)
        self._write('debug', output)

    def error(self, text: str):
        """用于记录刮削错误日志，面向用户"""
        output = f"[{self._now()}] [ERROR] {text}"
        print(output)

        self._write('log', output)
        self._write('debug', output)
