from typing import Dict

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar

from views.util import view_cursor


class UploadProgressItem(QWidget):
    remove_item_signal = Signal(QListWidgetItem, int)

    def __init__(self, item_view: QListWidgetItem, item: Dict, delete_icon_path='', index=0):
        super().__init__()
        self.item_view = item_view
        self.index = index

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
        self.close_icon_btn.clicked.connect(self.remove_at_index_list)
        self.close_icon_btn.setObjectName("")
        self.close_icon_btn.setObjectName("close_icon_btn")
        view_cursor(self.close_icon_btn)
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

        # size and speed
        size_speed_layout = QHBoxLayout()
        size_speed_layout.setAlignment(Qt.AlignLeft)
        size_speed_layout.setSpacing(10)
        size_label = QLabel(item.get('size'))
        size_speed_layout.addWidget(size_label)
        self.speed_label = QLabel('')
        size_speed_layout.addWidget(self.speed_label)

        right_layout.addLayout(size_speed_layout)

        # progress
        self.progress_widget = QProgressBar(self)
        self.progress_widget.setMinimumHeight(2)
        self.progress_widget.setMaximumHeight(2)
        self.progress_widget.setStyleSheet("""
            color: transparent;
        """)
        self.progress_widget.setRange(0, 100)
        self.progress_widget.setValue(100 if item['is_done'] else 0)
        right_layout.addWidget(self.progress_widget)
        layout.addLayout(right_layout)

    def remove_at_index_list(self):
        self.remove_item_signal.emit(self.item_view, self.index)
