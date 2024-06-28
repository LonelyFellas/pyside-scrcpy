from typing import Literal, Optional
import os
import subprocess
import sys
import time

from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QKeyEvent, QScreen
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QHBoxLayout, QFrame

from adb import Adbkit
from global_state import GlobalState
from views import find_window_by_title, embed_window, handle_startupinfo
from views.config import EXPEND_WIDTH, WIDTH_BUTTON
from views.control import Control
from views.upload_space import UploadSpace
from views.proxy_space import ProxySpace
from views.dialog_screen_shot import DialogScreenShot
from views.util import get_all_size

# 获取应用程序运行目录或打包后的临时目录
if hasattr(sys, '_MEIPASS'):
    application_path = os.path.join(sys._MEIPASS)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QMainWindow):
    space_attrs = ['proxy_space', 'upload_space']

    def __init__(self):
        super().__init__()
        self.scrcpy_addr = scrcpy_addr
        self.device = GlobalState().device
        self.buttons = []
        self.is_vertical_screen = is_vertical_screen
        self.rotation_number = scrcpy_size_num

        self.proxy_space = None
        self.upload_space = None
        self.last_expend_space = ''
        self.m_layout = None
        self.left_layout = None
        self.empty_widget = None
        self.control_widget = None  # 操作栏
        self.last_screen = None  # 记录上一次所在的显示屏
        self.scaling_factor = 0.0  # 缩放比
        self.width_scrcpy = 0  # scrcpy窗口的宽度
        self.width_win = 0  # 窗口的宽度
        self.height_win = 0  # 窗口的高度

        self.app_store_space = None

        self.setWindowTitle(scrcpy_title)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.m_layout = QHBoxLayout()
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)
        self.m_layout.setAlignment(Qt.AlignLeft)
        self.update_ui()
        self.app_store_expend = False
        self.proxy_expend = False
        self.upload_expend = False
        self.setStyleSheet(f"""
            QPushButton#outline_btn_none {{
                border: none;
                outline: none;
            }}
            QPushButton#outline_btn_none:hover {{
                background-color: #eee; 
                border-radius: 2px;
            }}
            QPushButton#outline_btn_none:pressed {{
                background-color: #ccc;
            }}
            QScrollBar:vertical
            {{
                width:12px;
                background:rgb(0,0,0,0%);
                margin:0px,0px,0px,0px;
                padding-top:12px;   /*上预留位置*/
                padding-bottom:12px;    /*下预留位置*/
            }}
             
            /*滚动条中滑块的样式*/
            QScrollBar::handle:vertical
            {{
                width:12px;
                background:rgb(0,0,0,25%);
                border-radius:4px;
                min-height:20px;
            }}
             
            /*鼠标触及滑块样式*/
            QScrollBar::handle:vertical:hover
            {{
                width:14px;
                background:rgb(0,0,0,50%);
                border-radius:4px;
                min-height:20;
            }}
             
            /*设置下箭头*/
            QScrollBar::add-line:vertical
            {{
                height:12px;
                width:4px;
                subcontrol-position:bottom;
            }}
             
            /*设置上箭头*/
            QScrollBar::sub-line:vertical
            {{
                height:12px;
                width:10px;
                subcontrol-position:top;
            }}
             
            /*设置下箭头:悬浮状态*/
            QScrollBar::add-line:vertical:hover
            {{
                height:12px;
                width:10px;
                subcontrol-position:bottom;
            }}
             
            /*设置上箭头：悬浮状态*/
            QScrollBar::sub-line:vertical:hover
            {{
                height:12px;
                width:10px;
                subcontrol-position:top;
            }}
             
            /*当滚动条滚动的时候，上面的部分和下面的部分*/
            QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical
            {{
                background:rgb(0,0,0,10%);
                border-radius:4px;
            }}

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
        if not self.is_vertical_screen:
            self.m_layout.removeWidget(self.empty_widget)
            self.m_layout.removeWidget(self.control_widget)

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

            self.m_layout.removeItem(self.left_layout)
            self.left_layout.deleteLater()
            self.left_layout = None
            self.remove_item_from_layout()

    def update_ui(self):
        print(self.devicePixelRatioF())
        print(self.devicePixelRatioF())
        self.is_vertical_screen = GlobalState().is_vertical_screen
        self.get_init_window_size()
        screen = QApplication.primaryScreen().availableGeometry()

        x = (screen.width() - self.width_win) // 2
        y = (screen.height() - self.height_win) // 2

        # 禁用最大化按钮和拉伸功能
        self.setFixedSize(self.width_win, self.height_win)
        self.setGeometry(x, y, self.width_win, self.height_win)

        if not self.is_vertical_screen:  # 横屏
            self.left_layout = QVBoxLayout()
            self.left_layout.setContentsMargins(0, 0, 0, 0)
            self.left_layout.setSpacing(0)
            self.left_layout.setAlignment(Qt.AlignTop)
            self.control_widget = Control(win_id=self.winId(), scrcpy_hwnd=scrcpy_hwnd,
                                          scaling_factor=self.scaling_factor, length=self.width_win)
            self.left_layout.addWidget(self.control_widget)
            self.empty_widget = QFrame()
            self.empty_widget.setFixedSize(self.width_scrcpy, self.height_win)
            self.left_layout.addWidget(self.empty_widget)
            self.m_layout.addLayout(self.left_layout)
        else:  # 竖屏
            self.empty_widget = QFrame()
            self.empty_widget.setFixedSize(self.width_scrcpy, self.height_win)
            self.m_layout.addWidget(self.empty_widget)
            self.control_widget = Control(win_id=self.winId(), scrcpy_hwnd=scrcpy_hwnd,
                                          scaling_factor=self.scaling_factor, length=self.height_win)
            self.m_layout.addWidget(self.control_widget)

        self.control_widget.create_sign.connect(self.expend_main_view)
        self.control_widget.screen_shop_sign.connect(self.on_screen_shop)
        self.control_widget.rotation_sign.connect(self.reset_window)
        self.central_widget.setLayout(self.m_layout)

    def reset_window(self):
        self.is_vertical_screen = GlobalState().is_vertical_screen
        sizes = self.get_rect(QApplication.primaryScreen())
        GlobalState().sizes = (sizes[2], sizes[3])
        # 重新对窗口进行赋值，因为某种特殊windows特有的原因。在切换显示屏的窗口和初始化创建的窗口不同。
        # 这边需要进一步同步窗口的大小
        self.get_init_window_size()
        # 投射子窗口
        embed_window(self.winId(), scrcpy_hwnd, sizes)
        self.clear_layout()
        self.update_ui()
        self.last_expend_space = ''

    def is_not_expend(self):
        return self.width() == self.width_win

    def get_init_window_size(self):
        global_width, global_height = GlobalState().sizes

        win_width = self.get_rect(QApplication.primaryScreen())[2] if global_width == 0 else global_width
        win_height = self.get_rect(QApplication.primaryScreen())[3] if global_height == 0 else global_height
        self.width_scrcpy = win_width
        self.width_win = win_width + (WIDTH_BUTTON if self.is_vertical_screen else 0)
        self.height_win = win_height + (0 if self.is_vertical_screen else WIDTH_BUTTON)

    def expend_window(self):
        if self.is_vertical_screen:
            self.setFixedSize(
                self.width_win + EXPEND_WIDTH if self.is_not_expend() else self.width_win,
                self.height_win
            )
        else:
            self.setFixedSize(
                self.width_win + EXPEND_WIDTH if self.is_not_expend() else self.width_win,
                self.width_win if self.is_not_expend() else self.height_win
            )

    def remove_widget_from_layout(self, widget_str=''):
        widget = getattr(self, widget_str, None)

        if widget is not None:
            self.m_layout.removeWidget(widget)
            widget.hide()
            setattr(self, widget_str, None)

    def remove_item_from_layout(self, widget_str: Optional[str] = None):
        space_attrs = [attr for attr in self.space_attrs if
                       attr != widget_str] if widget_str is not None else self.space_attrs

        for space_str in space_attrs:
            widget = getattr(self, space_str)
            if widget is not None:
                self.m_layout.removeWidget(widget)
                widget.hide()
                setattr(self, space_str, None)

    def expend_main_view(self, create_type: Literal['proxy_space', 'upload_space']):
        if self.last_expend_space == '' or self.last_expend_space == create_type:
            self.expend_window()

        if not self.is_not_expend():
            self.remove_item_from_layout(create_type)
            if create_type == 'proxy_space':
                self.proxy_space = ProxySpace(self,
                                              height=self.height_win if self.is_vertical_screen else self.width_win)
                self.m_layout.addWidget(self.proxy_space)
            else:
                self.upload_space = UploadSpace(self,
                                                height=self.height_win if self.is_vertical_screen else self.width_win)
                self.m_layout.addWidget(self.upload_space)
            self.last_expend_space = create_type
            return
        self.last_expend_space = ''
        self.remove_widget_from_layout(create_type)

    def open_upload_space_history_dialog(self):
        return self.upload_space and hasattr(self.upload_space,
                                             'history_dialog') and self.upload_space.history_dialog.isVisible()

    def resizeEvent(self, event):
        # 设置缩放比
        self.check_screen_change()
        super().resizeEvent(event)

    def moveEvent(self, event):
        self.check_screen_change()
        super().moveEvent(event)
        # 检查窗口位置是否超出屏幕
        self.ensure_window_within_screen()

    def ensure_window_within_screen(self):
        """
        检查窗口是否上下位置超出了屏幕
        :return:
        """
        # 初始化当前屏幕
        current_screen = QApplication.primaryScreen()
        # 获取窗口的几何信息
        window_rect = self.geometry()

        # 获取当前屏幕的几何信息
        screen_rect = current_screen.geometry()

        # 调整窗口位置，确保它在垂直方向上在屏幕内
        if window_rect.top() < screen_rect.top():
            self.move(window_rect.left(), screen_rect.top())
        elif window_rect.bottom() > screen_rect.bottom():
            self.move(window_rect.left(), screen_rect.bottom() - window_rect.height())

    def check_screen_change(self):
        # 获取当前主屏幕信息
        main_screen = QApplication.primaryScreen()
        current_screen = main_screen
        # 检查窗口当前所在的屏幕
        for screen in QApplication.screens():
            if screen.geometry().contains(self.geometry().center()):
                current_screen = screen
                break

        # 如果窗口移动到了新的屏幕
        if self.last_screen != current_screen:
            self.last_screen = current_screen
            sizes = self.get_rect(current_screen)

            GlobalState().sizes = (sizes[2], sizes[3])
            # 重新对窗口进行赋值，因为某种特殊windows特有的原因。在切换显示屏的窗口和初始化创建的窗口不同。
            # 这边需要进一步同步窗口的大小
            self.get_init_window_size()
            self.setFixedSize(self.width_win, self.height_win)
            # 投射子窗口
            embed_window(self.winId(), scrcpy_hwnd, sizes)

    def get_rect(self, main_screen: QScreen):
        screen_dpi = main_screen.physicalDotsPerInch()
        self.scaling_factor = screen_dpi / 96.0
        sizes = get_all_size(self.is_vertical_screen, self.scaling_factor)
        scale = sizes[2] / sizes[3]
        real_height = main_screen.geometry().height()
        # 处理2k，4k的窗口太小的问题
        if sizes[3] / real_height > 0.3:
            sizes[3] = real_height * 0.5
            sizes[2] = sizes[3] * scale
        return sizes


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
    # 启用高 DPI 支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # 设置高 DPI 感知属性
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    _, scrcpy_title, scrcpy_addr, token, env_id = sys.argv
    global_state = GlobalState()
    device = Adbkit(scrcpy_addr)
    scrcpy_size_num = device.query_system_orientation()
    is_vertical_screen = scrcpy_size_num == 0 or scrcpy_size_num == 2
    # 打开scrcpy dev模式下
    scrcpy_hwnd = open_scrcpy()
    app = QApplication([])

    # 初始化全局状态
    global_state.init(token, env_id, application_path, is_vertical_screen, scrcpy_size_num, device)
    window = MainWindow()
    # 打开窗口
    window.show()

    app.exec()
