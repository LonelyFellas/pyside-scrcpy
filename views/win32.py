from typing import Tuple

import win32gui
import win32con

import ctypes
from ctypes import wintypes

# 加载 User32 和 Shcore 库
user32 = ctypes.WinDLL('user32')
shcore = ctypes.WinDLL('Shcore')

# 定义所需的常量
MONITOR_DEFAULTTONEAREST = 2

# 定义函数和参数类型
shcore.GetScaleFactorForMonitor.argtypes = [wintypes.HMONITOR, ctypes.POINTER(ctypes.c_int)]
shcore.GetScaleFactorForMonitor.restype = ctypes.c_long  # 使用 ctypes.c_long 来表示 HRESULT


def get_monitor_scale_factor(hwnd) -> float:
    # 获取窗口所在的监视器
    hmonitor = user32.MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)

    # 准备一个 int 变量用于存储缩放因子
    scale_factor = ctypes.c_int()

    # 调用 GetScaleFactorForMonitor
    result = shcore.GetScaleFactorForMonitor(hmonitor, ctypes.byref(scale_factor))
    if result == 0:  # S_OK == 0
        print(f"Scale Factor: {scale_factor.value}%")
        return scale_factor.value / 100
    else:
        print("Failed to get scale factor, HRESULT:", result)
        return 1


def find_window_by_title(title: str):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        raise Exception(f"Window with title '{title}' not found!")
    return hwnd


def set_window_pos(child_hwnd: int, sizes: Tuple[int, int, int, int]):
    win32gui.SetWindowPos(child_hwnd, None, sizes[0], sizes[1], sizes[2], sizes[3],
                          win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE)


def embed_window(parent_hwnd: int, child_hwnd: int, sizes: Tuple[int, int, int, int]):
    win32gui.SetParent(child_hwnd, parent_hwnd)
    win32gui.SetWindowLong(child_hwnd, win32con.GWL_STYLE, win32con.WS_VISIBLE | win32con.WS_CHILD)
    monitor_scale_factor = get_monitor_scale_factor(parent_hwnd)
    set_window_pos(child_hwnd, (0, 0, int(sizes[2] * monitor_scale_factor), int(sizes[3] * monitor_scale_factor)))
