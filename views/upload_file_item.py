from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QListWidgetItem

from views.util import view_cursor


class FileItem(QWidget):
    remove_item_signal = Signal(QListWidgetItem, QPushButton, str)

    def __init__(self, item_view: QListWidgetItem, item, delete_icon_path=''):
        super().__init__()
        self.item_view = item_view
        self.item = item
        layout = QHBoxLayout()

        right_layout = QHBoxLayout()
        right_layout.setAlignment(Qt.AlignLeft)

        # cover
        file_cover = QLabel()
        icon_pixmap = QPixmap(item['cover']).scaled(30, 30, aspectMode=Qt.KeepAspectRatio)
        file_cover.setPixmap(icon_pixmap)
        right_layout.addWidget(file_cover)

        # name
        info_layout = QVBoxLayout()
        file_name = QLabel(item['filename'].split('/')[-1])
        info_layout.addWidget(file_name)

        # size and date
        size_date_layout = QHBoxLayout()
        size_date_layout.setAlignment(Qt.AlignLeft)
        size_date_layout.setSpacing(20)
        file_size = QLabel(item['size'])
        size_date_layout.addWidget(file_size)
        file_size = QLabel(item['date'])
        size_date_layout.addWidget(file_size)

        info_layout.addLayout(size_date_layout)

        right_layout.addLayout(info_layout)

        layout.addLayout(right_layout)

        # delete icon
        self.delete_icon_btn = QPushButton()
        self.delete_icon_btn.setFixedSize(50, 30)
        self.delete_icon_btn.setObjectName("delete_icon_btn")
        self.delete_icon_btn.setStyleSheet("""
            #delete_icon_btn {
                border: none;
                outline: none;
                width: 50px;
                height: 30px;
                border-radius: 4px;
            }
            #delete_icon_btn:hover {
                background-color: rgba(200, 200, 200, 0.5); 
            }
            #delete_icon_btn:pressed {
                background-color: rgba(200, 200, 200, 0.7); 
            }
        """)
        self.delete_icon_btn.setIcon(QIcon(delete_icon_path))
        self.delete_icon_btn.setIconSize(QSize(15, 15))
        self.delete_icon_btn.clicked.connect(self.remove_item)
        view_cursor(self.delete_icon_btn)

        layout.addWidget(self.delete_icon_btn)

        self.setLayout(layout)

    def remove_item(self):
        # 发送自定义信号，通知父控件删除该项
        self.remove_item_signal.emit(self.item_view, self.delete_icon_btn, self.item['filename'])



