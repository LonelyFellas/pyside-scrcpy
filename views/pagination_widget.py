import os
from math import ceil
from typing import TypedDict, Optional

from PySide6.QtCore import QSize, Signal, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QGraphicsOpacityEffect

from global_state import GlobalState
from views.util import view_cursor


class OptionDict(TypedDict, total=False):
    page_no: Optional[int]
    page_size: Optional[int]
    page_sum: Optional[int]


class PaginationWidget(QWidget):
    prev_signal = Signal()
    next_signal = Signal()

    def __init__(self, quantity=0, page_no=1, page_size=10, page_sum=0):
        super().__init__()
        self.setFixedHeight(35)
        self.setContentsMargins(0, 0, 0, 0)
        self.application_path = GlobalState().root_path
        self.page_no = page_no
        self.page_size = page_size
        self.page_sum = page_sum
        self.page_pages = ceil(page_sum / page_size)

        layout = QHBoxLayout()
        self.total_label = QLabel(f"总数：{quantity} 条")
        self.page_label = QLabel(str(self.page_no))

        self.prev_button = QPushButton()
        self.prev_button.setIcon(QIcon(os.path.join(self.application_path, 'images', 'prev_page.png')))
        self.prev_button.setObjectName("page_btn")
        if self.allow_prev():
            self.prev_button.setProperty("page_default_btn", "true")
            view_cursor(self.prev_button)
        else:
            self.prev_button.setProperty("disabled_btn", 'true')

        self.prev_button.setIconSize(QSize(24, 24))
        self.prev_button.clicked.connect(self.prev_func)
        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon(os.path.join(self.application_path, 'images', 'next_page.png')))
        self.next_button.setObjectName("page_btn")
        if self.allow_next():
            self.prev_button.setProperty("page_default_btn", "true")
            view_cursor(self.next_button)
        else:
            self.next_button.setProperty("disabled_btn", 'true')
        self.next_button.setIconSize(QSize(24, 24))
        self.next_button.clicked.connect(self.next_func)

        page_layout = QHBoxLayout()
        page_layout.addWidget(self.total_label)
        page_layout.addStretch()
        page_layout.addWidget(self.prev_button)
        page_layout.addWidget(self.page_label)
        page_layout.addWidget(self.next_button)

        layout.addLayout(page_layout)

        per_page_label = QLabel(f"{self.page_size}条/页")
        layout.addWidget(per_page_label)
        self.setStyleSheet("""
            QPushButton#page_btn {
                outline: none;
                border: none;
            }
            QPushButton[disabled_btn="true"] {
                outline: none;
                border: none;
            }
            QPushButton[page_default_btn="true"] {
                border: none;
                outline: none;
            }
            QPushButton[page_default_btn="true"]:hover {
                background-color: #eee; 
                border-radius: 2px;
            }
            QPushButton[page_default_btn="true"]:pressed {
                background-color: #ccc;
            }
        """)
        self.update_ui()
        self.setLayout(layout)

    def update_ui(self):
        if self.allow_prev():
            self.prev_button.setProperty("page_default_btn", "true")
            view_cursor(self.prev_button)

        else:
            self.prev_button.setProperty("disabled_btn", 'true')
            view_cursor(self.prev_button, cursor=Qt.ForbiddenCursor)

        # 更新样式
        self.prev_button.style().unpolish(self.prev_button)
        self.prev_button.style().polish(self.prev_button)
        if self.allow_next():
            self.next_button.setProperty("page_default_btn", "true")
            view_cursor(self.next_button)
        else:
            self.next_button.setProperty("disabled_btn", 'true')
            view_cursor(self.next_button, cursor=Qt.ForbiddenCursor)
        # 更新样式
        self.next_button.style().unpolish(self.next_button)
        self.next_button.style().polish(self.next_button)

    def allow_prev(self):
        return self.page_no != 1

    def allow_next(self):
        return self.page_sum != 0 and self.page_pages != self.page_no

    # 更新配置
    def set_option(self, option: OptionDict):
        self.page_no = option.get('page_no', self.page_no)
        self.page_size = option.get('page_size', self.page_size)
        self.page_sum = option.get('page_sum', self.page_sum)
        self.page_pages = ceil(self.page_sum / self.page_size)
        self.update_ui()

    # 上一页
    def prev_func(self):
        if self.page_no > 1:
            self.page_no -= 1
            self.page_label.setText(str(self.page_no))
            self.prev_signal.emit()
            self.update_ui()

    # 下一页
    def next_func(self):
        if self.page_pages > self.page_no:
            self.page_no += 1
            self.page_label.setText(str(self.page_no))
            self.next_signal.emit()
            self.update_ui()

    def set_sum_item(self, quantity: int):
        self.total_label.setText(f'总数：{quantity} 条')
