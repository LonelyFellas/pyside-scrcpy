import win32gui
import win32con

from views.config import HEIGHT_WINDOW, SCRCPY_WIDTH


def find_window_by_title(title: str):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        raise Exception(f"Window with title '{title}' not found!")
    return hwnd


def set_window_pos(child_hwnd: int, is_vertical: bool):
    width = SCRCPY_WIDTH
    height = HEIGHT_WINDOW
    top = 0

    if not is_vertical:
        width = HEIGHT_WINDOW
        height = SCRCPY_WIDTH
        top = 40

    win32gui.SetWindowPos(child_hwnd, None, 0, top, width, height, win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE)


def embed_window(parent_hwnd: int, child_hwnd: int, is_vertical: bool):
    win32gui.SetParent(child_hwnd, parent_hwnd)
    win32gui.SetWindowLong(child_hwnd, win32con.GWL_STYLE, win32con.WS_VISIBLE | win32con.WS_CHILD)

    set_window_pos(child_hwnd, is_vertical)
