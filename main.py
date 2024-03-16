import multiprocessing
import webview

from yolib import Helper

Helper.init()


def evaluate_js(window_):
    """在api之后加载的js函数"""
    window_.evaluate_js(
        """
        init();
        window_event_init();
        """
    )


if __name__ == '__main__':
    multiprocessing.freeze_support()
    from api import window, api

    # 配置文件只在启动时初始化一次，刮削子进程中忽略
    api.config_init()

    Helper.logging.debug('加载GUI界面...')
    webview.start(evaluate_js, window, debug=True)
