from typing import Literal, Optional
import os
import subprocess
import sys
import time

import shiboken6
from PySide6.QtCore import QSize, Qt, Slot
from PySide6.QtGui import QIcon, QCursor, QKeyEvent
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFrame

from adb import Adbkit
from global_state import GlobalState
from views import find_window_by_title, embed_window, handle_startupinfo
from views.config import WIDTH_WINDOW, HEIGHT_WINDOW, SCRCPY_WIDTH, EXPEND_WIDTH
from views.control import Control
from views.upload_space import UploadSpace
from views.proxy_space import ProxySpace
from views.dialog_screen_shot import DialogScreenShot
from views.util import palette_bg_color

# 获取应用程序运行目录或打包后的临时目录
if hasattr(sys, '_MEIPASS'):
    application_path = os.path.join(sys._MEIPASS)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QWidget):
    space_attrs = ['proxy_space', 'upload_space']

    def __init__(self):
        super().__init__()
        self.scrcpy_addr = scrcpy_addr
        self.device = GlobalState().get_device()
        self.buttons = []
        self.is_vertical_screen = is_vertical_screen
        self.rotation_number = scrcpy_size_num

        self.proxy_space = None
        self.upload_space = None
        self.last_expend_space = ''
        self.layout = None
        self.left_layout = None
        self.empty_widget = None
        self.control_widget = None

        self.app_store_space = None

        self.setWindowTitle(scrcpy_title)
        self.layout = QHBoxLayout()
        self.update_ui()
        self.app_store_expend = False
        self.proxy_expend = False
        self.upload_expend = False
        self.setStyleSheet("""
            QPushButton#outline_btn_none {
                border: none;
                outline: none;
            }
            QPushButton#outline_btn_none:hover {
                background-color: #eee; 
                border-radius: 2px;
            }
            QPushButton#outline_btn_none:pressed {
                background-color: #ccc;
            }
        """)

    # 监听键盘的事件
    def keyPressEvent(self, event: QKeyEvent):
        keycode = event.key()
        modifiers = QApplication.keyboardModifiers()
        shift_pressed = modifiers & Qt.ShiftModifier
        self.send_key_to_android(keycode, shift_pressed)

    # 对键盘的输入发送abd的指令
    def send_key_to_android(self, keycode, shift_pressed):
        # A mapping of PySide6 keycodes to Android keycodes
        key_mapping = {
            Qt.Key_A: (29, 45),  # Android keycode for 'A' (shift: 29 + shift)
            Qt.Key_B: (30, 46),
            Qt.Key_C: (31, 47),
            Qt.Key_D: (32, 48),
            Qt.Key_E: (33, 49),
            Qt.Key_F: (34, 50),
            Qt.Key_G: (35, 51),
            Qt.Key_H: (36, 52),
            Qt.Key_I: (37, 53),
            Qt.Key_J: (38, 54),
            Qt.Key_K: (39, 55),
            Qt.Key_L: (40, 56),
            Qt.Key_M: (41, 57),
            Qt.Key_N: (42, 58),
            Qt.Key_O: (43, 59),
            Qt.Key_P: (44, 60),
            Qt.Key_Q: (45, 61),
            Qt.Key_R: (46, 62),
            Qt.Key_S: (47, 63),
            Qt.Key_T: (48, 64),
            Qt.Key_U: (49, 65),
            Qt.Key_V: (50, 66),
            Qt.Key_W: (51, 67),
            Qt.Key_X: (52, 68),
            Qt.Key_Y: (53, 69),
            Qt.Key_Z: (54, 70),
            Qt.Key_0: (7, 7),  # Android keycode for '0'
            Qt.Key_1: (8, 8),
            Qt.Key_2: (9, 9),
            Qt.Key_3: (10, 10),
            Qt.Key_4: (11, 11),
            Qt.Key_5: (12, 12),
            Qt.Key_6: (13, 13),
            Qt.Key_7: (14, 14),
            Qt.Key_8: (15, 15),
            Qt.Key_9: (16, 16),
            Qt.Key_Escape: 111,
            Qt.Key_Tab: 61,
            Qt.Key_Backspace: 67,
            Qt.Key_Return: 66,
            Qt.Key_Enter: 66,
            Qt.Key_Shift: 59,
            Qt.Key_Control: 113,
            Qt.Key_Alt: 57,
            Qt.Key_Space: 62,
            Qt.Key_Left: 21,
            Qt.Key_Up: 19,
            Qt.Key_Right: 22,
            Qt.Key_Down: 20,
            Qt.Key_Delete: 112,
            Qt.Key_Home: 3,
            Qt.Key_End: 123,
            Qt.Key_PageUp: 92,
            Qt.Key_PageDown: 93,
            Qt.Key_F1: 131,
            Qt.Key_F2: 132,
            Qt.Key_F3: 133,
            Qt.Key_F4: 134,
            Qt.Key_F5: 135,
            Qt.Key_F6: 136,
            Qt.Key_F7: 137,
            Qt.Key_F8: 138,
            Qt.Key_F9: 139,
            Qt.Key_F10: 140,
            Qt.Key_F11: 141,
            Qt.Key_F12: 142,
            Qt.Key_Semicolon: 74,  # ;
            Qt.Key_Equal: 70,  # =
            Qt.Key_Comma: 55,  # ,
            Qt.Key_Minus: 69,  # -
            Qt.Key_Period: 56,  # .
            Qt.Key_Slash: 76,  # /
            Qt.Key_BracketLeft: 71,  # [
            Qt.Key_Backslash: 73,  # \
            Qt.Key_BracketRight: 72,  # ]
            Qt.Key_Apostrophe: 75,  # '
            Qt.Key_QuoteLeft: 68,  # `
            Qt.Key_CapsLock: 115,
            Qt.Key_NumLock: 143,
            Qt.Key_ScrollLock: 116,
            Qt.Key_Insert: 124,
            Qt.Key_Pause: 121,
            # Add more mappings as needed
        }

        if keycode in key_mapping:
            android_keycode = key_mapping[keycode]
            if isinstance(android_keycode, tuple):
                android_keycode = android_keycode[1] if shift_pressed else android_keycode[0]
            command = f"adb -s {self.scrcpy_addr} shell input keyevent {android_keycode}"
            subprocess.run(command, shell=True)
        else:
            print(f"未映射的键码: {keycode}")

    def on_screen_shop(self):

        dialog = DialogScreenShot(self, scrcpy_addr)
        dialog.exec()

    def clear_layout(self):
        if self.is_vertical_screen:
            print("竖屏")
            self.layout.removeWidget(self.empty_widget)
            self.layout.removeWidget(self.control_widget)

            self.empty_widget.deleteLater()
            self.control_widget.deleteLater()
            self.empty_widget = None
            self.control_widget = None

            self.remove_item_from_layout()
        else:
            self.left_layout.removeWidget(self.control_widget)

            self.empty_widget.deleteLater()
            self.control_widget.deleteLater()
            self.empty_widget = None
            self.control_widget = None

            self.layout.removeItem(self.left_layout)
            self.left_layout.deleteLater()
            self.left_layout = None
            self.remove_item_from_layout()

    def update_ui(self):

        self.is_vertical_screen = GlobalState().get_is_vertical_screen()
        width_window = WIDTH_WINDOW if self.is_vertical_screen else HEIGHT_WINDOW
        height_window = HEIGHT_WINDOW if self.is_vertical_screen else WIDTH_WINDOW
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - width_window) // 2
        y = (screen.height() - height_window) // 2

        # 禁用最大化按钮和拉伸功能
        self.setFixedSize(width_window, height_window)
        self.setGeometry(x, y, width_window, height_window)

        if not self.is_vertical_screen:  # 横屏
            self.left_layout = QVBoxLayout()
            self.left_layout.setContentsMargins(0, 0, 0, 0)
            self.left_layout.setSpacing(0)
            self.left_layout.setAlignment(Qt.AlignTop)

            self.control_widget = Control(win_id=self.window().winId(), scrcpy_hwnd=scrcpy_hwnd)
            self.left_layout.addWidget(self.control_widget)
            self.empty_widget = QFrame()
            self.empty_widget.setFixedSize(HEIGHT_WINDOW, SCRCPY_WIDTH)
            self.left_layout.addWidget(self.empty_widget)
            self.layout.addLayout(self.left_layout)
        else:  # 竖屏
            self.empty_widget = QFrame()
            self.empty_widget.setFixedSize(SCRCPY_WIDTH, HEIGHT_WINDOW)
            self.layout.addWidget(self.empty_widget)
            self.control_widget = Control(win_id=self.window().winId(), scrcpy_hwnd=scrcpy_hwnd)
            self.layout.addWidget(self.control_widget)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignLeft)
        self.control_widget.create_sign.connect(self.expend_main_view)
        self.control_widget.screen_shop_sign.connect(self.on_screen_shop)
        self.control_widget.rotation.connect(self.reset_window)
        self.setLayout(self.layout)

    def reset_window(self):
        self.clear_layout()
        self.update_ui()
        self.last_expend_space = ''

    def is_not_expend(self):
        return self.width() == (WIDTH_WINDOW if self.is_vertical_screen else HEIGHT_WINDOW)

    def expend_window(self):
        if self.is_vertical_screen:
            self.setFixedSize(
                WIDTH_WINDOW + EXPEND_WIDTH if self.is_not_expend() else WIDTH_WINDOW,
                HEIGHT_WINDOW
            )
        else:
            self.setFixedSize(
                HEIGHT_WINDOW + EXPEND_WIDTH if self.is_not_expend() else HEIGHT_WINDOW,
                HEIGHT_WINDOW if self.is_not_expend() else WIDTH_WINDOW
            )

    def remove_widget_from_layout(self, widget_str=''):
        widget = getattr(self, widget_str, None)

        if widget is not None:
            self.layout.removeWidget(widget)
            widget.hide()
            setattr(self, widget_str, None)

    def remove_item_from_layout(self, widget_str: Optional[str] = None):
        space_attrs = [attr for attr in self.space_attrs if
                       attr != widget_str] if widget_str is not None else self.space_attrs

        for space_str in space_attrs:
            widget = getattr(self, space_str)
            if widget is not None:
                self.layout.removeWidget(widget)
                widget.hide()
                setattr(self, space_str, None)

    @Slot(str)
    def expend_main_view(self, create_type: Literal['proxy_space', 'upload_space']):
        if self.last_expend_space == '' or self.last_expend_space == create_type:
            self.expend_window()

        if not self.is_not_expend():
            self.remove_item_from_layout(create_type)
            if create_type == 'proxy_space':
                self.proxy_space = ProxySpace(self)
                self.layout.addWidget(self.proxy_space)
            else:
                self.upload_space = UploadSpace(self)
                self.layout.addWidget(self.upload_space)
            self.last_expend_space = create_type
            return
        self.last_expend_space = ''
        self.remove_widget_from_layout(create_type)

    def open_upload_space_history_dialog(self):
        return self.upload_space and hasattr(self.upload_space,
                                             'history_dialog') and self.upload_space.history_dialog.isVisible()


def open_scrcpy() -> int:
    """
    start a window of scrcpy
    打开scrcpy第三方窗口
    :return: int
    """
    scrcpy_process = subprocess.Popen(
        ['scrcpy', '-s', scrcpy_addr, '--window-width', '1', '--window-height', '1', '--max-size', '1080'],
        **handle_startupinfo())
    time.sleep(1)

    try:
        hwnd = find_window_by_title(title=scrcpy_title)
    except Exception as e:
        print(f'Error: {e}')
        scrcpy_process.terminate()
        exit(1)
    return hwnd


if __name__ == "__main__":
    _, scrcpy_title, scrcpy_addr, token, env_id, window_size = sys.argv
    global_state = GlobalState()
    device = Adbkit(scrcpy_addr)
    scrcpy_size_num = device.query_system_orientation()
    is_vertical_screen = scrcpy_size_num == 0 or scrcpy_size_num == 2
    # 初始化全局状态
    global_state.init(token, env_id, application_path, is_vertical_screen, scrcpy_size_num, device, window_size)
    scrcpy_hwnd = open_scrcpy()
    app = QApplication([])
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    window = MainWindow()
    window.show()

    embed_window(window.winId(), scrcpy_hwnd, is_vertical_screen)

    app.exec()
