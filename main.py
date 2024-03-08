import os
import webview

from api import api, debug


def evaluate_js(window):
    window.evaluate_js(
        r"""
        init()
        """
    )


if __name__ == '__main__':
    debug.logging.debug('加载GUI界面...')

    window = webview.create_window('日语学习刮削器', 'gui/window.html', js_api=api)
    webview.start(evaluate_js, window, debug=True)
