import os
import re
import subprocess
from datetime import datetime
from typing import Dict, Optional

import requests
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog

from global_state import GlobalState
from views.config import WIDTH_WINDOW
from views.worker_thread import WorkerThread

FILE_NAME = f'scrrenshot_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.png'


class DialogScreenShot(QDialog):
    def __init__(self, parent=None, scrcpy_addr=None, width=WIDTH_WINDOW):
        super().__init__(parent)
        self.pic_url = ''
        self.scrcpy_addr = scrcpy_addr
        self.adb_capture_screen_shot()
        self.is_open_save_file_dialog = False
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setModal(True)
        self.setGeometry(parent.x() + width + 10, parent.y() + 30, 100, 196)

        layout = QVBoxLayout(self)

        # 添加QLabel用于展示的图片
        self.img_label = QLabel(self)
        self.update_img()
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

    def update_img(self):
        """更新 QLabel 上的图像"""
        pixmap = QPixmap()
        if self.pic_url != '':
            img_data = self.get_image_data(self.pic_url)
            pixmap.loadFromData(img_data)
        self.img_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    @staticmethod
    def get_image_data(url):
        """从 URL 下载图像"""
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to download image: {response.status_code}")

    def adb_capture_screen_shot(self):
        # 异步adb截屏，不阻塞主线程
        result = subprocess.Popen(
            ["adb", '-s', GlobalState().device.serial, "shell", "screencap", '-p', f"/sdcard/Pictures/{FILE_NAME}"],
            creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
        if result.stderr:
            print(f"Error capturing screenshot: {result.stderr}")
            return

        # 获取后端云机详情，拿取图片网络资源地址
        token = GlobalState().token
        env_id = GlobalState().env_id
        self.shop_data = WorkerThread(token, f'env/getById?id={env_id}', data=None)
        self.shop_data.data_fetched.connect(self.adb_capture_screen_shot_finished)
        self.shop_data.start()

    def adb_capture_screen_shot_finished(self, data: Dict):
        if data is not None and 'screenShot' in data:
            self.pic_url = data.get('screenShot')
            self.update_img()

    def download_image(self):
        """
        保存截屏的功能
        :return:
        """
        self.is_open_save_file_dialog = True
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(download_dir, exist_ok=True)
        pic_name = os.path.join(download_dir, FILE_NAME)
        # 替换更加清晰的图片到本地
        self.pic_url = re.sub(r"level=2", "level=3", self.pic_url)
        response = requests.get(self.pic_url, stream=True)
        if response.status_code == 200:
            file_path, _ = QFileDialog.getSaveFileName(self, "保存图片",
                                                       f"{pic_name}",
                                                       "PNG Files (*png);;AllFiles(*)")

            if file_path:
                # 开始保存到本地
                with open(file_path, "wb") as f:
                    f.write(response.content)
                self.accept()
            else:  # 对话框取消关闭截图的dialog
                self.accept()
        else:
            raise Exception(f"Failed to download image: {response.status_code}")

    def delay_close_img(self):
        if not self.is_open_save_file_dialog:
            self.accept()
