from typing import Literal

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from global_state import GlobalState
from views import embed_window
from views.config import SCRCPY_WIDTH, HEIGHT_WINDOW, WIDTH_WINDOW
from views.control_btn_widget import ControlBtnWidget
from views.util import palette_bg_color


class Control(QWidget):
    create_sign = Signal(str)
    screen_shop_sign = Signal()
    rotation = Signal()

    def __init__(self, win_id=0, scrcpy_hwnd=-1):
        super().__init__()
        self.layout = None
        self.is_vertical_screen = GlobalState().is_vertical_screen
        if self.is_vertical_screen:
            self.setFixedSize(
                WIDTH_WINDOW - SCRCPY_WIDTH, HEIGHT_WINDOW)
            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignTop)
            layout.setContentsMargins(0, 10, 0, 10)
        else:
            self.setFixedSize(HEIGHT_WINDOW,
                              WIDTH_WINDOW - SCRCPY_WIDTH)
            layout = QHBoxLayout()
            layout.setAlignment(Qt.AlignLeft)
            layout.setContentsMargins(10, 0, 10, 0)

        self.device = GlobalState().device
        palette_bg_color(self, color='#d5d8e1')

        btn_arr = [{
            "title": "旋转",
            "icon": 'rotary.png',
            "on_click": lambda: self.on_rotate_screen(win_id, scrcpy_hwnd),
        }, {
            "title": "截屏",
            "icon": 'screen-shot.png',
            "on_click": lambda: self.screen_shop_sign.emit()
        }, {
            "title": "上传",
            "icon": 'file-upload.png',
            "on_click": lambda: self.create_view('upload_space')
        }, {
            "title": "音量",
            "icon": 'volume-up.png',
            "on_click": lambda: self.on_keyevent('KEYCODE_VOLUME_UP')
        }, {
            "title": "音量",
            "icon": 'volume-down.png',
            "on_click": lambda: self.on_keyevent('KEYCODE_VOLUME_DOWN')
        }, {
            "title": "代理",
            "icon": 'speed.png',
            "on_click": lambda: self.create_view('proxy_space')
        }, {
            "title": "更多",
            "icon": 'more.png',
            "on_click": None
        }, {
            "title": "",
            "icon": 'latest-up.png',
            "on_click": lambda: self.on_keyevent('4')
        }, {
            "title": "",
            "icon": 'main-menu.png',
            "on_click": lambda: self.on_keyevent('3')
        }, {
            "title": "",
            "icon": 'all-process.png',
            "on_click": lambda: self.on_keyevent('187')
        }, {
            "title": "应用",
            "icon": 'app.png',
            "on_click": None
        }]
        for index, btn in enumerate(btn_arr):
            btn_widget = ControlBtnWidget(self, btn)

            if index == 7:
                layout.addSpacing(50 if self.is_vertical_screen else 20)
            elif index == 8 or index == 9:
                layout.addSpacing(0)
            elif len(btn_arr) - 1 == index:
                layout.addStretch(60)
            elif index != 0:
                layout.addSpacing(5)
            layout.addWidget(btn_widget)

            self.setLayout(layout)

    def create_view(self, create_type: Literal['proxy_space', 'upload_space']):
        self.create_sign.emit(create_type)

    def on_keyevent(self, keycode):
        self.device.shell(['input', 'keyevent', keycode])

    def on_rotate_screen(self, win_id, scrcpy_hwnd):
        self.device.shell(['settings', 'put', 'system', 'accelerometer_rotation', '0'])

        rotation_num = GlobalState().orientation
        if rotation_num == 3:
            rotation_num = 0
        else:
            rotation_num += 1
        command = ["settings", "put", "system", "user_rotation",
                   f'{rotation_num}']
        result = self.device.shell(command)
        if result.returncode != 0:
            raise RuntimeError(f"Error executing screen rotation command: {result.stderr}")
        else:
            is_vertical_screen = rotation_num == 0 or rotation_num == 2
            GlobalState().orientation(rotation_num)
            GlobalState().is_vertical_screen(is_vertical_screen)
            embed_window(win_id, scrcpy_hwnd, is_vertical_screen)
            self.rotation.emit()
