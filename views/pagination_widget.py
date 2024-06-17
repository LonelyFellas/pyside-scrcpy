import os

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

from global_state import GlobalState
from views.util import view_cursor


class PaginationWidget(QWidget):
    def __init__(self, quantity=0):
        super().__init__()
        self.setFixedHeight(35)
        self.setContentsMargins(0, 0, 0, 0)
        self.application_path = GlobalState().get_root_path()

        layout = QHBoxLayout()
        self.total_label = QLabel(f"总数：{quantity}")
        page_label = QLabel("1")

        prev_button = QPushButton()
        prev_button.setIcon(QIcon(os.path.join(self.application_path, 'images', 'prev_page.png')))
        prev_button.setObjectName("outline_btn_none")
        prev_button.setIconSize(QSize(24, 24))
        view_cursor(prev_button)
        next_button = QPushButton()
        next_button.setIcon(QIcon(os.path.join(self.application_path, 'images', 'next_page.png')))
        next_button.setObjectName("outline_btn_none")
        next_button.setIconSize(QSize(24, 24))
        view_cursor(next_button)

        page_layout = QHBoxLayout()
        page_layout.addWidget(self.total_label)
        page_layout.addStretch()
        page_layout.addWidget(prev_button)
        page_layout.addWidget(page_label)
        page_layout.addWidget(next_button)

        layout.addLayout(page_layout)

        per_page_label = QLabel("10条/页")
        layout.addWidget(per_page_label)
        self.setLayout(layout)

    def set_sum_item(self, quantity: int):
        self.total_label.setText(f'总数：{quantity}')

    # def next_page(self):
