from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from global_state import GlobalState
from views.spin_label import SpinFrame
from views.util import images_path


class EmptyView(QWidget):
    def __init__(self, width=0, height=0, loading=True, empty_w=0, empty_h=0, font_size=18):
        super().__init__()
        layout = QVBoxLayout()
        self.setFixedSize(width, height)
        self.placeholder_label = QLabel()
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        # 是否有loading效果
        self.loading = loading
        pixmap = QPixmap(images_path(GlobalState().root_path, 'empty.png'))  # 替换为你的图片路径
        resized_pixmap = pixmap.scaled(empty_w, empty_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.placeholder_label.setPixmap(resized_pixmap)
        layout.addWidget(self.placeholder_label)
        empty_label = QLabel("暂无数据")
        empty_label.setStyleSheet(f"font-weight: bold; font-size: {font_size}px; color: gray")
        empty_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(empty_label)
        layout.setAlignment(Qt.AlignCenter)
        if loading:
            self.spin_frame = SpinFrame(self)

        self.setLayout(layout)

    def loading_done(self):
        """
        一般页面线程任务或异步完成后，不需要loading的效果，这里进行停用隐藏
        :return:
        """
        if self.loading:
            self.spin_frame.hide()
