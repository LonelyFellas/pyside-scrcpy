import os
from functools import partial

from PySide6.QtCore import QRect, QSize, Slot, QPoint
from PySide6.QtGui import Qt, QIcon
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QFileDialog, \
    QListWidget, QListWidgetItem
from views.config import UPLOAD_WIDTH
from views.confirm_msg_box import ConfirmMsgBox, ConfirmationParams
from views.dialog import CustomDialogModal
from views.upload_file_item import FileItem
from views.util import images_path
from views.upload_dialog import UploadDialog
from views.divider import Divider


class UploadSpace(QFrame):
    def __init__(self, parent=None, width_window=0, application_path='', token='', env_id=2):
        super().__init__(parent)
        self.setObjectName("upload_space_frame")
        self.setGeometry(width_window, 10, UPLOAD_WIDTH - 10, parent.size().height() - 20)
        self.layout = QVBoxLayout(self)
        self.application_path = application_path
        self.create_top_view()
        self.create_main_header_view()
        self.create_files_list_view()
        self.layout.setAlignment(Qt.AlignTop)
        self.main_window = self.window()
        self.setStyleSheet("""
            #upload_space_frame {
                background-color: white; 
                border: 1px solid gray;
            } 
            QPushButton#upload_upload_btn {
                border: none;
                outline: none;
                background-color: rgb(64, 150, 255);
                color: white;
                border-radius: 3px;
            } 
            QPushButton#upload_upload_btn:hover {
                background-color: rgb(44, 130, 255)  
            }
            QPushButton#upload_upload_btn:pressed {
                background-color: rgb(22, 110, 255) 
            }
        """)

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
        edit_btn.setToolTip("修改储存位置")
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
        self.history_upload_btn.setToolTip("上传队列")
        self.history_upload_btn.setIconSize(QSize(30, 30))
        self.history_upload_btn.setFixedSize(50, 25)
        header_right_layout.addWidget(self.history_upload_btn)
        self.info_btn = QPushButton("")
        self.info_btn.clicked.connect(self.open_upload_info)
        self.info_btn.setIcon(QIcon(images_path(self.application_path, 'info.png')))
        self.info_btn.setToolTip("注意事项")
        self.info_btn.setIconSize(QSize(30, 30))
        self.info_btn.setFixedSize(50, 25)
        header_right_layout.addWidget(self.info_btn)
        upload_btn = QPushButton("上传文件")
        upload_btn.setObjectName("upload_upload_btn")
        upload_btn.setIcon(QIcon(images_path(self.application_path, 'file-upload-white.png')))
        upload_btn.setIconSize(QSize(30, 30))
        upload_btn.setFixedSize(100, 25)
        header_right_layout.addWidget(upload_btn)
        header_layout.addLayout(header_right_layout)
        self.layout.addLayout(header_layout)

    def create_files_list_view(self):
        self.files_list = QListWidget(self)
        path = os.path.join(self.application_path, 'images', 'flc-file-icon.png')
        delete_icon_path = os.path.join(self.application_path, 'images', 'delete.png')
        items = [
            (path, "Petco1.png", "0.92KB"),
            (path, "Petco2.png", "0.92KB"),
            (path, "Petco3.png", "0.92KB"),
            (path, "Petco4.png", "0.92KB"),
            (path, "Petco5.png", "0.92KB"),
            (path, "Petco6.png", "0.92KB"),
            (path, "Petco7.png", "0.92KB"),
            (path, "Petco8.png", "0.92KB"),
            (path, "Petco9.png", "0.92KB"),
            (path, "Petco11.png", "0.92KB"),
            (path, "Petco22.png", "0.92KB"),
            (path, "Petco33.png", "0.92KB"),
            (path, "Petco44.png", "0.92KB"),
        ]

        for icon, name, size in items:
            item = QListWidgetItem(self.files_list)
            item_widget = FileItem(item, icon, name, size, delete_icon_path)
            item_widget.remove_item_signal.connect(self.remove_item)
            item.setSizeHint(item_widget.sizeHint())
            self.files_list.setItemWidget(item, item_widget)

        self.layout.addWidget(self.files_list)

    def remove_item(self, item: QListWidgetItem, item_delete_btn: QPushButton):
        button_position = item_delete_btn.mapToGlobal(item_delete_btn.rect().center())
        print(button_position)
        message_box = ConfirmMsgBox(self,
                                    ConfirmationParams(position=button_position,
                                                       on_yes=partial(self.remove_item_yes, item),
                                                       on_no=self.remove_item_no, title="删除文件",
                                                       text="确定要删除该文件吗，删除后将不可恢复"))
        message_box.exec_()
    def remove_item_yes(self, item: QListWidgetItem):
        row = self.files_list.row(item)
        self.files_list.takeItem(row)

    @staticmethod
    def remove_item_no():
        print("已取消")

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
