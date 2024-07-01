import os
from queue import Queue
import re
import subprocess
from functools import partial
from typing import Optional, Literal

from PySide6.QtCore import QRect, QSize, Slot, QThread, Signal, QTimer
from PySide6.QtGui import Qt, QIcon, QCursor
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QFileDialog, \
    QListWidget, QListWidgetItem, QSpacerItem, QRadioButton, QButtonGroup

from global_state import GlobalState
from views import handle_startupinfo
from views.config import UPLOAD_WIDTH, EXPEND_WIDTH, HEIGHT_WINDOW
from views.confirm_msg_box import ConfirmMsgBox, ConfirmationParams
from views.dialog import CustomDialogModal
from views.empty import EmptyView
from views.pagination_widget import PaginationWidget
from views.upload_file_item import FileItem
from views.upload_local_space import UploadLocalSpace
from views.upload_trans_space import UploadTransSpace
from views.util import images_path
from views.upload_dialog import UploadDialog
from adb import AdbPushThread


class UploadSpace(QFrame):
    def __init__(self, parent=None, height=0):
        super().__init__(parent)
        self.scrcpy_addr = GlobalState().device.serial
        self.application_path = GlobalState().root_path
        self.sum = 0
        self.setObjectName("upload_space_frame")
        self.setContentsMargins(0, 0, 0, 10)
        self.setFixedSize(EXPEND_WIDTH, height)
        self.items = []
        self.threads = Queue()
        self.loading = False
        self.pageNo = 1
        self.pageSize = 10

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 10, 0, 0)

        # radio buttons 创建两个button
        self.radio_btn_layout = QHBoxLayout()
        self.radio_btn_layout.setSpacing(20)
        self.radio_btn_layout.setAlignment(Qt.AlignLeft)
        self.radio_btn_layout.setContentsMargins(10, 0, 0, 0)
        trans_btn = QRadioButton("中转站推送")
        self.radio_btn_layout.addWidget(trans_btn)
        trans_btn.setGeometry(10, 10, 100, 30)
        trans_btn.setChecked(True)
        local_btn = QRadioButton("本地直传")
        self.radio_btn_layout.addWidget(local_btn)
        local_btn.setGeometry(100, 10, 100, 30)
        # 设置 QRadioButton 的光标样式，使鼠标经过时变为指针
        trans_btn.setCursor(QCursor(Qt.PointingHandCursor))
        local_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # 创建按钮组来管理 QRadioButton
        button_group = QButtonGroup(self)
        button_group.addButton(trans_btn)
        button_group.addButton(local_btn)

        # 连接信号和槽
        trans_btn.toggled.connect(self.show_trans_view)
        local_btn.toggled.connect(self.show_local_view)

        self.layout.addLayout(self.radio_btn_layout)
        self.trans_view = UploadTransSpace()
        self.layout.addWidget(self.trans_view)
        self.local_view = UploadLocalSpace()
        self.local_view.hide()
        self.layout.addWidget(self.local_view)

        self.setLayout(self.layout)

    def show_trans_view(self):
        self.trans_view.show()
        self.local_view.hide()

    def show_local_view(self):
        self.trans_view.hide()
        self.local_view.show()
