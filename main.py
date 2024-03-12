import webview

from api import debug, window


def evaluate_js(window_):
    """在api之后加载的js函数"""
    window_.evaluate_js(
        r"""
        init();
        window_event_init();
        """
    )


if __name__ == '__main__':
    debug.logging.debug('加载GUI界面...')

    webview.start(evaluate_js, window, debug=True)
