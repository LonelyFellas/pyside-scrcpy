import win32gui
import win32con


def find_window_by_title(title: str):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        raise Exception(f"Window with title '{title}' not found!")
    return hwnd


def get_window_rect(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    return rect[2] - rect[0], rect[3] - rect[1]


def get_client_rect(hwnd):
    rect = win32gui.GetClientRect(hwnd)
    return rect[2] - rect[0], rect[3] - rect[1]


def set_window_pos(child_hwnd: int, is_vertical: bool):
    width = 400
    height = 702
    top = 0

    if not is_vertical:
        width = 702
        height = width
        top = 50

    win32gui.SetWindowPos(child_hwnd, None, 0, top, width, height, win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE)


def embed_window(parent_hwnd: int, child_hwnd: int, is_vertical: bool):
    win32gui.SetParent(child_hwnd, parent_hwnd)
    win32gui.SetWindowLong(child_hwnd, win32con.GWL_STYLE, win32con.WS_VISIBLE | win32con.WS_CHILD)

    set_window_pos(child_hwnd, is_vertical)
