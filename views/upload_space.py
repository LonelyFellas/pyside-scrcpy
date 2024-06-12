from PySide6.QtCore import QRect, QSize, Slot, QPoint
from PySide6.QtGui import Qt, QIcon
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QFileDialog
from views.config import UPLOAD_WIDTH
from views.dialog import CustomDialogModal
from views.util import images_path
from views.upload_dialog import UploadDialog


class UploadSpace(QFrame):
    def __init__(self, parent=None, width_window=0, application_path='', token='', env_id=2):
        super().__init__(parent)

        self.setGeometry(width_window, 10, UPLOAD_WIDTH - 10, parent.size().height() - 20)
        self.layout = QVBoxLayout(self)
        self.application_path = application_path
        self.create_top_view()
        self.create_main_header_view()
        self.layout.setAlignment(Qt.AlignTop)
        self.main_window = self.window()

    def create_top_view(self):
        top_layout = QVBoxLayout()
        top_layout.setGeometry(QRect(0, 0, UPLOAD_WIDTH - 10, 41))
        top_layout.setAlignment(Qt.AlignTop)
        top_layout.setContentsMargins(0, 0, 0, 0)  # 去除布局边距
        top_layout.setSpacing(5)  # 设置布局间距为0
        li1 = QLabel("⭐ 文件上传完成后可在云手机文件管理中找到")
        li1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)  # 设置大小策略

        top_layout.addWidget(li1)
        top_second_layout = QHBoxLayout()
        top_second_layout.setAlignment(Qt.AlignLeft)
        li2_text = QLabel('⭐ 文件存储位置：Files/Download')
        edit_btn = QPushButton()
        edit_btn.setIcon(QIcon(images_path(self.application_path, 'edit.png')))
        edit_btn.setIconSize(QSize(30, 30))
        edit_btn.setFixedSize(50, 25)
        top_second_layout.addWidget(li2_text)
        top_second_layout.addWidget(edit_btn)
        top_layout.addLayout(top_second_layout)
        self.layout.addLayout(top_layout)

    def create_main_header_view(self):
        header_layout = QHBoxLayout()
        self.left_label = QLabel("全部文件（1）")
        header_layout.addWidget(self.left_label)
        header_right_layout = QHBoxLayout()
        self.history_upload_btn = QPushButton("上传")
        self.history_upload_btn.clicked.connect(self.open_upload_dialog)
        self.history_upload_btn.setIcon(QIcon(images_path(self.application_path, 'file-upload.png')))
        self.history_upload_btn.setIconSize(QSize(30, 30))
        self.history_upload_btn.setFixedSize(50, 25)
        header_right_layout.addWidget(self.history_upload_btn)
        info_btn = QPushButton("提示")
        info_btn.clicked.connect(self.open_upload_info)
        info_btn.setIcon(QIcon(images_path(self.application_path, 'info.png')))
        info_btn.setIconSize(QSize(30, 30))
        info_btn.setFixedSize(50, 25)
        header_right_layout.addWidget(info_btn)
        upload_btn = QPushButton("上传文件")
        upload_btn.setIcon(QIcon(images_path(self.application_path, 'upload.png')))
        upload_btn.setIconSize(QSize(30, 30))
        upload_btn.setFixedSize(100, 25)
        header_right_layout.addWidget(upload_btn)
        header_layout.addLayout(header_right_layout)
        self.layout.addLayout(header_layout)

    @Slot()
    def open_upload_dialog(self):
        self.history_dialog = UploadDialog(self)
        self.main_window.layout().addWidget(self.history_dialog)

    @Slot()
    def open_upload_info(self):
        print(self.x())
        self.info_dialog = CustomDialogModal(x=self.x(), y=90, width=300, height=50)
        self.info_dialog.show()
        main_layout = self.info_dialog.setup_layout()
        label = QLabel("上传文件的历史记录")
        label.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); border-radius: 4px;")
        main_layout.layout().addWidget(self.info_dialog)

    def moveEvent(self, event):
        print(event)
