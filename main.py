import os
import subprocess
import sys

from PySide6.QtCore import QSize, Qt, QPoint, QEvent
from PySide6.QtGui import QIcon, QCursor, QKeyEvent
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout

from views import find_window_by_title, embed_window, handle_startupinfo
from views.config import WIDTH_WINDOW, HEIGHT_WINDOW, WIDTH_BUTTON, HEIGHT_BUTTON, ICON_SIZE, SCRCPY_WIDTH, \
    APP_STORE_WIDTH, \
    WIDTH_WINDOW_V, HEIGHT_WINDOW_V, TOP_V, PROXY_WIDTH, UPLOAD_WIDTH
from views.upload_space import UploadSpace
from views.util import images_path
from views.apk_store_space import ApkStoreSpace
from views.proxy_space import ProxySpace
from views.dialog_screen_shot import DialogScreenShot
from views.win_event import desktop_to_android_keycode

# 获取应用程序运行目录或打包后的临时目录
if hasattr(sys, '_MEIPASS'):
    application_path = os.path.join(sys._MEIPASS)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QMainWindow):
    expend_attrs = ['app_store_expend', 'proxy_expend', 'upload_expend']
    space_attrs = ['app_store_space', 'proxy_space', 'upload_space.py']

    def __init__(self):
        super().__init__()
        self.scrcpy_addr = scrcpy_addr
        self.buttons = []
        self.is_vertical_screen = is_vertical_screen
        self.rotation_number = scrcpy_size_num
        self.app_store_space = None
        self.proxy_space = None
        self.upload_space = None
        self.setWindowTitle(scrcpy_title)
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

    def update_ui(self):
        (width_window,
         height_window,
         rotary_x,
         rotary_y,
         shot_x, shot_y,
         upload_x,
         upload_y,
         v_up_x,
         v_up_y,
         v_down_x,
         v_down_y,
         speed_x,
         speed_y,
         more_x,
         more_y,
         back_x,
         back_y,
         main_x,
         main_y,
         all_x,
         all_y,
         app_x,
         app_y) = self.config_fn().values()
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - width_window) // 2
        y = (screen.height() - height_window) // 2

        # 禁用最大化按钮和拉伸功能
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(width_window, height_window)
        self.setGeometry(x, y, width_window, height_window)

        btn_arr = [{
            "title": "旋转",
            "x": rotary_x,
            "y": rotary_y,
            "icon_path": images_path(application_path, 'rotary.png'),
            "on_click": self.on_rotate_screen,
        }, {
            "title": "截屏",
            "x": shot_x,
            "y": shot_y,
            "icon_path": images_path(application_path, 'screen-shot.png'),
            "on_click": self.on_screen_shop
        }, {
            "title": "上传",
            "x": upload_x,
            "y": upload_y,
            "icon_path": images_path(application_path, 'file-upload.png'),
            "on_click": self.create_upload_files
        }, {
            "title": "音量",
            "x": v_up_x,
            "y": v_up_y,
            "icon_path": images_path(application_path, 'volume-up.png'),
            "on_click": lambda: self.on_keyevent('KEYCODE_VOLUME_UP')
        }, {
            "title": "音量",
            "x": v_down_x,
            "y": v_down_y,
            "icon_path": images_path(application_path, 'volume-down.png'),
            "on_click": lambda: self.on_keyevent('KEYCODE_VOLUME_DOWN')
        }, {
            "title": "代理",
            "x": speed_x,
            "y": speed_y,
            "icon_path": images_path(application_path, 'speed.png'),
            "on_click": self.create_proxy_view
        }, {
            "title": "更多",
            "x": more_x,
            "y": more_y,
            "icon_path": images_path(application_path, 'more.png'),
            "on_click": None
        }, {
            "title": "",
            "x": back_x,
            "y": back_y,
            "icon_path": images_path(application_path, 'latest-up.png'),
            "on_click": lambda: self.on_keyevent('4')
        }, {
            "title": "",
            "x": main_x,
            "y": main_y,
            "icon_path": images_path(application_path, 'main-menu.png'),
            "on_click": lambda: self.on_keyevent('3')
        }, {
            "title": "",
            "x": all_x,
            "y": all_y,
            "icon_path": images_path(application_path, 'all-process.png'),
            "on_click": lambda: self.on_keyevent('187')
        }, {
            "title": "应用",
            "x": app_x,
            "y": app_y,
            "icon_path": images_path(application_path, 'app.png'),
            "on_click": self.on_apk_store
        }]

        for btn in btn_arr:
            title = btn.get("title")
            y_btn = btn.get("y")
            x_btn = btn.get("x")
            icon_btn = btn.get('icon_path')
            on_click = btn.get('on_click')

            button = QPushButton(title, self)
            button.setGeometry(x_btn, y_btn, WIDTH_BUTTON, HEIGHT_BUTTON)
            button.setIcon(QIcon(icon_btn))
            button.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
            button.setText(title)  # 设置按钮文字
            button.clicked.connect(on_click)
            button.setCursor(QCursor(Qt.PointingHandCursor))
            self.buttons.append(button)
            if title == '更多' or title == '应用':
                button.setEnabled(False)
                button.setCursor(QCursor(Qt.ForbiddenCursor))

        self.create_upload_files()

    def on_rotate_screen(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        subprocess.run(['adb', '-s', scrcpy_addr, 'shell', 'settings', 'put', 'system', 'accelerometer_rotation', '0'],
                       **handle_startupinfo())

        if self.rotation_number == 3:
            self.rotation_number = 0
        else:
            self.rotation_number += 1
        command = ["adb", '-s', scrcpy_addr, "shell", "settings", "put", "system", "user_rotation",
                   f'{self.rotation_number}']
        result = subprocess.run(command, **handle_startupinfo())
        if result.returncode != 0:
            raise RuntimeError(f"Error executing screen rotation command: {result.stderr}")
        else:
            self.rotation_number = int(query_scrcpy_system_size())
            self.is_vertical_screen = self.rotation_number == 0 or self.rotation_number == 2
            embed_window(window.winId(), scrcpy_hwnd, self.is_vertical_screen)
            self.reset_window()

    def config_fn(self):
        return {
            "width_window": WIDTH_WINDOW if self.is_vertical_screen else WIDTH_WINDOW_V,
            "height_window": HEIGHT_WINDOW if self.is_vertical_screen else HEIGHT_WINDOW_V,
            "rotary_x": SCRCPY_WIDTH if self.is_vertical_screen else 10,
            "rotary_y": 10 if self.is_vertical_screen else TOP_V,
            'shot_x': SCRCPY_WIDTH if self.is_vertical_screen else 70,
            'shot_y': 50 if self.is_vertical_screen else TOP_V,
            "upload_x": SCRCPY_WIDTH if self.is_vertical_screen else 130,
            "upload_y": 90 if self.is_vertical_screen else TOP_V,
            'v_up_x': SCRCPY_WIDTH if self.is_vertical_screen else 190,
            'v_up_y': 130 if self.is_vertical_screen else TOP_V,
            'v_down_x': SCRCPY_WIDTH if self.is_vertical_screen else 250,
            'v_down_y': 170 if self.is_vertical_screen else TOP_V,
            'speed_x': SCRCPY_WIDTH if self.is_vertical_screen else 310,
            'speed_y': 210 if self.is_vertical_screen else TOP_V,
            'more_x': SCRCPY_WIDTH if self.is_vertical_screen else 370,
            'more_y': 250 if self.is_vertical_screen else TOP_V,
            'back_x': SCRCPY_WIDTH if self.is_vertical_screen else 450,
            'back_y': 350 if self.is_vertical_screen else TOP_V,
            'main_x': SCRCPY_WIDTH if self.is_vertical_screen else 510,
            'main_y': 390 if self.is_vertical_screen else TOP_V,
            'all_x': SCRCPY_WIDTH if self.is_vertical_screen else 570,
            'all_y': 430 if self.is_vertical_screen else TOP_V,
            'app_x': SCRCPY_WIDTH if self.is_vertical_screen else 653,
            'app_y': 660 if self.is_vertical_screen else TOP_V
        }

    def on_key_press(self, event):
        command = ["adb", '-s', self.scrcpy_addr, "shell", "input", 'keyevent',
                   f'{desktop_to_android_keycode.get(event.keycode)}']
        subprocess.run(command, **handle_startupinfo())

    def on_keyevent(self, keycode):
        command = ["adb", '-s', self.scrcpy_addr, "shell", "input", 'keyevent', keycode]
        subprocess.run(command, **handle_startupinfo())

    def other_close_space(self, expend_attr, space_attr):
        # Exclude the specified expend_attr and space_attr
        other_expend_attrs = [attr for attr in self.expend_attrs if attr != expend_attr]
        other_space_attrs = [attr for attr in self.space_attrs if attr != space_attr]

        self.close_space(other_expend_attrs, other_space_attrs)

        setattr(self, expend_attr, not getattr(self, expend_attr, False))

    def close_space(self, e_attrs, s_attrs):
        for attr in e_attrs:
            setattr(self, attr, False)

        for attr in s_attrs:
            space = getattr(self, attr, None)
            if space is not None:
                space.hide()

    def reset_window(self):
        """
        清空所有视图，并回到起始窗口
        :return:
        """
        for button in self.buttons:
            button.deleteLater()

        self.close_space(self.expend_attrs, self.space_attrs)
        self.buttons.clear()
        self.update_ui()
        self.show()

    def expend_window_size(self, expend_width=0, expend_bool=False):
        # 以下几行是对spk_store组件展开或者不展开窗口大小的计算
        size = self.size()
        height = size.height()
        width_window = self.config_fn().get('width_window')
        height_window = self.config_fn().get('height_window')
        app_store_width_window = width_window + (expend_width if expend_bool else 0)
        height_apk = height if self.is_vertical_screen else (702 if expend_bool else height_window)
        self.setFixedSize(app_store_width_window, height_apk)

        return width_window

    def on_apk_store(self):
        self.other_close_space('app_store_expend', 'app_store_space')

        width_window = self.expend_window_size(APP_STORE_WIDTH, self.app_store_expend)

        # 如果是不展开的，限免的ApkStoreSpace将不在进行渲染，直接return
        if not self.app_store_expend and self.app_store_space is not None:
            self.app_store_space.hide()
            return

        # 设置小部件的布局
        self.app_store_space = ApkStoreSpace(self, width_window, application_path, token)
        self.app_store_space.show()
        self.app_store_space.raise_()

    def create_proxy_view(self):
        """
        点击代理按钮，显示代理的view
        :return:
        """
        # 关闭其他展开的扩展的视图
        self.layout = QVBoxLayout(self)
        self.other_close_space('proxy_expend', 'proxy_space')

        width_window = self.expend_window_size(PROXY_WIDTH, self.proxy_expend)
        # 设置小部件的布局
        self.proxy_space = ProxySpace(self, width_window, application_path=application_path, token=token, env_id=env_id)
        self.layout.addWidget(self.proxy_space)
        self.proxy_space.show()

    def create_upload_files(self):
        """
        点击上传文件按钮
        :return:
        """
        self.other_close_space('upload_expend', 'upload_space')
        width_window = self.expend_window_size(UPLOAD_WIDTH, self.upload_expend)
        self.upload_space = UploadSpace(self, width_window, application_path=application_path, scrcpy_addr=self.scrcpy_addr)
        self.upload_space.show()

    def open_upload_space_history_dialog(self):
        return self.upload_space and hasattr(self.upload_space,
                                             'history_dialog') and self.upload_space.history_dialog.isVisible()


def query_scrcpy_system_size():
    """
    获取当前的屏幕是竖屏还是横屏 0，2为竖屏，1，3为横屏
    :return: str
    """
    output_size = subprocess.check_output(
        ['adb', '-s', scrcpy_addr, 'shell', 'settings', 'get', 'system', 'user_rotation'],
        creationflags=subprocess.CREATE_NO_WINDOW, shell=True,
    )
    try:
        return output_size.decode('utf-8').strip()
    except Exception as e:
        print(f'Error: {e}')
        return '1'


def open_scrcpy() -> int:
    # """
    # start a window of scrcpy
    # 打开scrcpy第三方窗口
    # :return: int
    # """
    # scrcpy_process = subprocess.Popen(
    #     ['scrcpy', '-s', scrcpy_addr, '--window-width', '1', '--window-height', '1', '--max-size', '1080'],
    #     **handle_startupinfo())
    # time.sleep(1)

    try:
        hwnd = find_window_by_title(title=scrcpy_title)
    except Exception as e:
        print(f'Error: {e}')
        # scrcpy_process.terminate()
        exit(1)
    return hwnd


if __name__ == "__main__":
    _, scrcpy_title, scrcpy_addr, token, env_id, env = sys.argv
    # scrcpy_size_num = int(query_scrcpy_system_size())
    scrcpy_size_num = 1
    # is_vertical_screen = scrcpy_size_num == 0 or scrcpy_size_num == 2
    is_vertical_screen = True
    if env == 'pro':
        scrcpy_hwnd = open_scrcpy()
    app = QApplication([])
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    window = MainWindow()
    window.show()

    if env == 'pro':
        embed_window(window.winId(), scrcpy_hwnd, is_vertical_screen)

    app.exec()
