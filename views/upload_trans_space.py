from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel

from views.util import palette_bg_color


class UploadTransSpace(QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        title = QLabel("请从文件中转站推送到云手机（云手机默认存储路径：/sdcard/Download/）")
        self.layout.addWidget(title)
        info_frame = QFrame(self)
        self.layout.addWidget(info_frame)
