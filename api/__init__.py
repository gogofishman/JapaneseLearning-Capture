# 前后端通信api
import os
import importlib
import sys
import multiprocessing
import webview
from types import ModuleType

import scraper
from api.config import Config
from .get_jav_number import get_jav_number
from .videoClass import Video
from .window import setup_all_windows_borderless, window_resize_start, window_resize_update
from .scraper_run_func import scraper_run
from yolib import Helper


class Api(Config):
    video_format: tuple = ('.mp4', '.mkv', '.avi', '.rmvb', '.flv', '.mov', '.rm', '.wvm')
    module_list: dict[str, ModuleType] = {}
    """保存所有刮削器的文件模块字典"""
    window_max: bool = False
    scraper_run_subProcess: multiprocessing.Process = None

    def __init__(self):
        super().__init__()

        # 加载全部Scraper文件
        path = Helper.path.data_dir.joinpath('plugins')

        for file in path.glob('*.py'):
            module_name = file.stem
            if module_name == 'example':
                continue

            module = importlib.import_module(f'plugins.{module_name}')

            # 检查模块是否含Scraper类
            try:
                instance = module.Scraper()
                instance = None
            except Exception:
                continue

            Api.module_list[module_name] = module
            Helper.logging.debug(f'加载刮削器 "{module_name}" 成功!')

    def get_all_scraper(self) -> list[str]:
        """获取所有刮削器"""
        return list(self.module_list.keys())

    def search_file(self) -> dict:
        """查找文件"""

        path = self.input_path()

        if not os.path.exists(path) or path.startswith(("\\", "/")):
            return {}

        video_dict = {}
        for file in os.listdir(path):

            file_path = os.path.join(path, file)

            if not file.endswith(Api.video_format):
                continue
            size = os.stat(file_path).st_size / (1024 ** 2)

            if self.ignore_100mb():
                if size < 100:
                    continue

            # 解析番号
            jav_number = get_jav_number(file)
            video_dict[file] = {
                "path": file_path,
                "size": round(size / 1024, 2),
                "jav_number": jav_number[0],
                "uncensored": jav_number[1],
                "subtitle": jav_number[2],
                "long_jav_number": jav_number[3]
            }
        return video_dict

    def scraper_run(self, video_title: str, video_title_suffix: str, file_path: str, scraper: str = 'JavDB') -> int:
        """
        开始刮削
        :param video_title_suffix:后缀，如-C,-U
        :param video_title:视频标题
        :param file_path:视频源文件完整地址
        :param scraper:刮削器名称
        :return: 0 成功 ，-1 失败 ，1 有误
        """
        queue = multiprocessing.Queue()

        Api.scraper_run_subProcess = multiprocessing.Process(target=scraper_run,
                                                              args=(queue, self, video_title, video_title_suffix,
                                                                    file_path, scraper))
        Api.scraper_run_subProcess.start()

        while True:
            result = queue.get()

            # 数字表示刮削结束，字符串则实时向发送进度信息
            if isinstance(result, int):
                return result

            window.evaluate_js(f"console.log('{result}')")

    def test_translate(self, text):
        return scraper.translator.translate(text)

    def window_minimize(self):
        window.minimize()

    def window_maximize(self):
        if Api.window_max:
            window.restore()
        else:
            window.maximize()

        Api.window_max = not Api.window_max

    def window_close(self):
        window.destroy()
        self.scraper_run_subProcess.terminate()
        sys.exit()

    def window_resize_start(self):
        window_resize_start(window)

    def window_resize_update(self, direction):
        window_resize_update(window, direction)


api = Api()
window = webview.create_window('', 'gui/window.html', js_api=api
                               , width=1024, height=650, frameless=True, easy_drag=False)
window.events.loaded += setup_all_windows_borderless
