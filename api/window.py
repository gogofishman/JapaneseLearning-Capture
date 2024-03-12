import os
import ctypes
from webview.window import FixPoint

point = ctypes.wintypes.POINT()
window_resize_start_point = ()
window_resize_start_size = ()


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


def get_mouse_position():
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


def window_resize_start(window):
    global window_resize_start_point
    global window_resize_start_size
    window_resize_start_point = get_mouse_position()
    window_resize_start_size = (window.width, window.height)


def window_resize_update(window, direction):
    point_now = get_mouse_position()

    if direction == 'left':
        window.resize(window_resize_start_size[0] + window_resize_start_point[0] - point_now[0],
                      window.height, FixPoint.EAST)
    elif direction == 'right':
        window.resize(window_resize_start_size[0] + point_now[0] - window_resize_start_point[0],
                      window.height, FixPoint.WEST)
    elif direction == 'top':
        window.resize(window.width,
                      window_resize_start_size[1] + window_resize_start_point[1] - point_now[1],
                      FixPoint.SOUTH)
    elif direction == 'bottom':
        window.resize(window.width,
                      window_resize_start_size[1] + point_now[1] - window_resize_start_point[1],
                      FixPoint.NORTH)
    elif direction == 'left-top':
        window.resize(window_resize_start_size[0] + window_resize_start_point[0] - point_now[0],
                      window_resize_start_size[1] + window_resize_start_point[1] - point_now[1],
                      FixPoint.SOUTH|FixPoint.EAST)
    elif direction == 'left-bottom':
        window.resize(window_resize_start_size[0] + window_resize_start_point[0] - point_now[0],
                      window_resize_start_size[1] + point_now[1] - window_resize_start_point[1],
                      FixPoint.NORTH|FixPoint.EAST)
    elif direction == 'right-top':
        window.resize(window_resize_start_size[0] + point_now[0] - window_resize_start_point[0],
                      window_resize_start_size[1] + window_resize_start_point[1] - point_now[1],
                      FixPoint.SOUTH|FixPoint.WEST)
    elif direction == 'right-bottom':
        window.resize(window_resize_start_size[0] + point_now[0] - window_resize_start_point[0],
                      window_resize_start_size[1] + point_now[1] - window_resize_start_point[1],
                      FixPoint.NORTH|FixPoint.WEST)
