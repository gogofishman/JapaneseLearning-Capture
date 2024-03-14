import multiprocessing
import webview

from api import debug, window
from helper.pathHelper import path_helper


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

    path_helper.init(__file__)

    debug.logging.debug('加载GUI界面...')

    webview.start(evaluate_js, window, debug=False)



