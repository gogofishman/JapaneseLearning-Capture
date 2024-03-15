import multiprocessing
import webview

from yolib import Helper


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
    Helper.init()

    from api import window

    Helper.logging.debug('加载GUI界面...')
    webview.start(evaluate_js, window, debug=False)
