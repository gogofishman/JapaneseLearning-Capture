import os
import webview

from api import api, debug


def setup_all_windows_borderless():
    """实现圆角窗口"""
    import ctypes
    import ctypes.wintypes
    import win32process, win32gui

    def DwmSetWindowAttribute(hwnd, attr, value, size=4):
        DwmSetWindowAttribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
        DwmSetWindowAttribute.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.DWORD, ctypes.c_void_p,
                                          ctypes.wintypes.DWORD]
        return DwmSetWindowAttribute(hwnd, attr, ctypes.byref(ctypes.c_int(value)), size)

    def ExtendFrameIntoClientArea(hwnd):
        class _MARGINS(ctypes.Structure):
            _fields_ = [("cxLeftWidth", ctypes.c_int),
                        ("cxRightWidth", ctypes.c_int),
                        ("cyTopHeight", ctypes.c_int),
                        ("cyBottomHeight", ctypes.c_int)]

        DwmExtendFrameIntoClientArea = ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea
        m = _MARGINS()
        m.cxLeftWidth = 1
        m.cxRightWidth = 1
        m.cyTopHeight = 1
        m.cyBottomHeight = 1
        return DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(m))

    def get_hwnds_for_pid(pid):
        hwnds = []

        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                found_tid, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnds.append(hwnd)
                return True

        win32gui.EnumWindows(callback, hwnds)
        return hwnds

    hwnds = get_hwnds_for_pid(os.getpid())
    print(hwnds)
    for hwnd in hwnds:
        DwmSetWindowAttribute(hwnd, 2, 2, 4)
        ExtendFrameIntoClientArea(hwnd)


def evaluate_js(window):
    """在api加载之后加载的js函数"""
    window.evaluate_js(
        r"""
        init()
        """
    )


if __name__ == '__main__':
    debug.logging.debug('加载GUI界面...')

    window = webview.create_window('日语学习刮削器', 'gui/window.html', js_api=api
                                   , width=1024, height=650, min_size=(650, 450), frameless=True, easy_drag=False)
    window.events.loaded += setup_all_windows_borderless
    webview.start(evaluate_js, window, debug=True)
