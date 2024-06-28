import os
import subprocess
from datetime import datetime
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog

from views.config import WIDTH_WINDOW


class DialogScreenShot(QDialog):
    def __init__(self, parent=None, scrcpy_addr=None):
        super().__init__(parent)
        self.pic_name = f'scrrenshot_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.png'
        self.scrcpy_addr = scrcpy_addr
        self.adb_capture_screen_shot()
        self.is_open_save_file_dialog = False
        self.setWindowFlag(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.setGeometry(parent.x() + WIDTH_WINDOW + 10, parent.y() + 30, 100, 196)

        layout = QVBoxLayout(self)

        # 添加QLabel用于展示的图片
        self.img_label = QLabel(self)
        pixmap = QPixmap(self.pic_name)
        self.img_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(self.img_label)

        # 创建水平居中的按钮
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        # 添加下载按钮
        self.download_btn = QPushButton("保存", self)
        self.download_btn.setFixedSize(80, 25)
        self.download_btn.setIcon(QIcon("./images/file-upload.png"))
        self.download_btn.clicked.connect(self.download_image)
        button_layout.addWidget(self.download_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        QTimer.singleShot(3000, self.delay_close_img)

    def adb_capture_screen_shot(self):
        """
        截屏并且拉取刚才截屏的图片放在页面展示
        :return:
        """
        result = subprocess.run(
            ["adb", '-s', self.scrcpy_addr, "shell", "screencap", '-p', f"/sdcard/Pictures/{self.pic_name}"],
            creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
        if result.stderr:
            print(f"Error capturing screenshot: {result.stderr}")
            return
        result = subprocess.run(
            ["adb", '-s', self.scrcpy_addr, "pull", f"/sdcard/Pictures/{self.pic_name}", os.getcwd()],
            creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
        if result.stderr:
            print(f"Error pulling screenshot: {result.stderr}")
            return

    def accept_and_delete_template_img(self):
        """
         模态框关闭后删除pull下来的为临时的图片
        :return:
        """
        self.accept()
        os.unlink(self.pic_name)

    def download_image(self):
        """
        保存截屏的功能
        :return:
        """
        self.is_open_save_file_dialog = True
        file_path, _ = QFileDialog.getSaveFileName(self, "保存图片",
                                                   f"{self.pic_name}",
                                                   "PNG Files (*png);;AllFiles(*)")
        if file_path:
            pixmap = self.img_label.pixmap()
            if pixmap:
                pixmap.save(file_path)
                self.accept_and_delete_template_img()
        else:  # 对话框取消关闭截图的dialog
            self.accept_and_delete_template_img()

    def delay_close_img(self):
        if not self.is_open_save_file_dialog:
            self.accept_and_delete_template_img()
