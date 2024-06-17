from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from global_state import GlobalState
from views.spin_label import SpinFrame
from views.util import images_path


class EmptyView(QWidget):
    def __init__(self, width=0, height=0, empty_w=0, empty_h=0):
        super().__init__()
        layout = QVBoxLayout()
        self.setFixedSize(width, height)
        self.placeholder_label = QLabel()
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(images_path(GlobalState().get_root_path(), 'empty.png'))  # 替换为你的图片路径
        resized_pixmap = pixmap.scaled(empty_w, empty_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.placeholder_label.setPixmap(resized_pixmap)
        layout.addWidget(self.placeholder_label)
        empty_label = QLabel("暂无数据")
        empty_label.setStyleSheet("font-weight: bold; font-size: 18px; color: gray")
        empty_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(empty_label)
        layout.setAlignment(Qt.AlignCenter)
        self.spin_frame = SpinFrame(self)

        self.setLayout(layout)
