from typing import Dict

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar


class UploadProgressItem(QWidget):
    def __init__(self, item_views: QListWidgetItem, item: Dict,  delete_icon_path=''):
        super().__init__()

        layout = QHBoxLayout(self)

        # cover
        file_cover = QLabel()
        icon_pixmap = QPixmap(item['cover']).scaled(30, 30, aspectMode=Qt.KeepAspectRatio)
        file_cover.setPixmap(icon_pixmap)
        layout.addWidget(file_cover)

        # right layout
        right_layout = QVBoxLayout()
        # right layout -- first
        right_first_layout = QHBoxLayout()
        name_label = QLabel(item.get('filename'))
        right_first_layout.addWidget(name_label)
        self.close_icon_btn = QPushButton()
        self.close_icon_btn.setFixedSize(15, 15)
        self.close_icon_btn.setObjectName("")
        self.close_icon_btn.setObjectName("close_icon_btn")
        self.close_icon_btn.setStyleSheet("""
            #close_icon_btn {
                border: none;
                outline: none;
                width: 40px;
                height: 30px;
                border-radius: 4px;
            }
            #close_icon_btn:hover {
                background-color: rgba(200, 200, 200, 0.5); 
            }
            #close_icon_btn:pressed {
                background-color: rgba(200, 200, 200, 0.7); 
            }
        """)
        self.close_icon_btn.setIcon(QIcon(delete_icon_path))
        right_first_layout.addWidget(self.close_icon_btn)
        right_layout.addLayout(right_first_layout)

        # size
        size_label = QLabel(item.get('size'))
        right_layout.addWidget(size_label)
        # progress
        self.progress_widget = QProgressBar(self)
        self.progress_widget.setMinimumHeight(2)
        self.progress_widget.setMaximumHeight(2)
        self.progress_widget.setStyleSheet("""
            color: transparent;
        """)
        self.progress_widget.setRange(0, 100)
        self.progress_widget.setValue(0)
        right_layout.addWidget(self.progress_widget)
        layout.addLayout(right_layout)



