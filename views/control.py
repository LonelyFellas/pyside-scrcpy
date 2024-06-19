from PySide6 import QtGui
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QPushButton

from global_state import GlobalState
from views import handle_startupinfo, embed_window
from views.config import SCRCPY_WIDTH, HEIGHT_WINDOW, WIDTH_WINDOW
from views.control_btn_widget import ControlBtnWidget
from views.util import palette_bg_color, images_path, img_label, spacer_item, view_cursor


class Control(QWidget):
    def __init__(self, win_id=0, scrcpy_hwnd=-1):
        super().__init__()
        self.setFixedSize(WIDTH_WINDOW - SCRCPY_WIDTH, HEIGHT_WINDOW)
        self.device = GlobalState().get_device()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setAlignment(Qt.AlignTop)
        palette_bg_color(self, color='#d5d8e1')

        btn_arr = [{
            "title": "旋转",
            "icon": 'rotary.png',
            "on_click": lambda: self.on_rotate_screen(win_id, scrcpy_hwnd),
        }, {
            "title": "截屏",
            "icon": 'screen-shot.png',
            # "on_click": self.on_screen_shop
        }, {
            "title": "上传",
            "icon": 'file-upload.png',
            # "on_click": self.create_upload_files
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
            # "on_click": self.create_proxy_view
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
            # "on_click": self.on_apk_store
        }]
        for index, btn in enumerate(btn_arr):
            btn_widget = ControlBtnWidget(self, btn)
            view_cursor(btn_widget)

            if index == 7:
                layout.addSpacing(60)
            if len(btn_arr) - 1 == index:
                layout.addStretch(60)
            layout.addWidget(btn_widget)

        self.setLayout(layout)

    def on_keyevent(self, keycode):
        self.device.shell(['input', 'keyevent', keycode])

    def reset_window(self):
        """
        清空所有视图，并回到起始窗口
        :return:
        """
        print()
        # for button in self.buttons:
        #     button.deleteLater()
        #
        # self.close_space(self.expend_attrs, self.space_attrs)
        # self.buttons.clear()
        # self.update_ui()
        # self.show()

    def on_rotate_screen(self, win_id, scrcpy_hwnd):
        self.device.shell(['settings', 'put', 'system', 'accelerometer_rotation', '0'])

        rotation_num = GlobalState().get_rotation_num()
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
            GlobalState().set_orientation(rotation_num)
            GlobalState().set_is_vertical_screen(is_vertical_screen)
            embed_window(win_id, scrcpy_hwnd, is_vertical_screen)
            self.reset_window()
