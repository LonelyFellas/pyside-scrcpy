from PySide6.QtCore import QRect, QSize, Slot, QPoint
from PySide6.QtGui import Qt, QIcon
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QFileDialog
from views.config import UPLOAD_WIDTH
from views.dialog import CustomDialogModal
from views.util import images_path
from views.upload_dialog import UploadDialog
from views.divider import Divider


class UploadSpace(QFrame):
    def __init__(self, parent=None, width_window=0, application_path='', token='', env_id=2):
        super().__init__(parent)
        self.setObjectName("upload_space_frame")
        self.setStyleSheet("#upload_space_frame {background-color: white; border: 1px solid gray;}")
        self.setGeometry(width_window, 10, UPLOAD_WIDTH - 10, parent.size().height() - 20)
        self.layout = QVBoxLayout(self)
        self.application_path = application_path
        self.create_top_view()
        self.create_main_header_view()
        self.layout.addWidget(Divider(self))
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
        self.history_upload_btn = QPushButton("")
        self.history_upload_btn.clicked.connect(self.open_upload_dialog)
        self.history_upload_btn.setIcon(QIcon(images_path(self.application_path, 'file-upload.png')))
        self.history_upload_btn.setIconSize(QSize(30, 30))
        self.history_upload_btn.setFixedSize(50, 25)
        header_right_layout.addWidget(self.history_upload_btn)
        self.info_btn = QPushButton("")
        self.info_btn.clicked.connect(self.open_upload_info)
        self.info_btn.setIcon(QIcon(images_path(self.application_path, 'info.png')))
        self.info_btn.setIconSize(QSize(30, 30))
        self.info_btn.setFixedSize(50, 25)
        header_right_layout.addWidget(self.info_btn)
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
        self.info_dialog = CustomDialogModal(x=604, y=100, width=300, height=120)
        main_layout = self.info_dialog.setup_layout()
        self.info_dialog.dialog.frame.setObjectName("info_main_layout_dialog")
        self.info_dialog.dialog.setStyleSheet(
            """
                QFrame#info_main_layout_dialog {
                    background-color: rgba(0, 0, 0, 0.4); 
                    border-radius: 4px; 
                    padding: 10px;
                }
                QLabel {
                    color: white;
                }
            """
        )
        main_layout.setAlignment(Qt.AlignTop)
        content_layout = QVBoxLayout()
        label1 = QLabel("上传文件须符合一下规则：")
        text2 = "⭐ 单次上传文件大小不能为0KB，不超过500MB，数量不超过50个"
        label2 = QLabel()
        formatted_text = text2[:20] + "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + text2[20:]
        label2.setText(formatted_text)
        label2.setWordWrap(True)
        label3 = QLabel("⭐ 文件名字符数小于60个字符(包含文件后缓)")
        label4 = QLabel("⭐ 文件名不包含单引号")
        content_layout.addWidget(label1)
        content_layout.addWidget(label2)
        content_layout.addWidget(label3)
        content_layout.addWidget(label4)
        main_layout.addLayout(content_layout)
        self.main_window.layout().addWidget(self.info_dialog)

    def moveEvent(self, event):
        print(event)
