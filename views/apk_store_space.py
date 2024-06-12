import re
import subprocess

import os

from PySide6.QtCore import Slot
from PySide6.QtGui import QCursor, Qt, QPalette, QColor
from PySide6.QtWidgets import QRadioButton, QButtonGroup, QFrame, QListWidget, QListWidgetItem, QLabel, QVBoxLayout

from views.spin_label import SpinFrame
from views.app_store_item import AppItem
from views.worker_thread import WorkerThread
from views.config import APP_STORE_WIDTH


class ApkStoreSpace(QFrame):
    def __init__(self, parent=None, width_window=0, application_path='./', token=''):
        super().__init__(parent)
        self.application_path = application_path
        self.token = token
        self.scrcpy_addr = parent.scrcpy_addr
        self.setGeometry(width_window, 10, APP_STORE_WIDTH - 10, parent.size().height() - 20)

        palette = self.palette()
        self.setPalette(palette)

        # 设置边框
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(1)

        # 设置边框颜色
        palette.setColor(QPalette.WindowText, QColor("#336699"))
        self.setPalette(palette)

        # 创建两个 QRadioButton
        radio_button1 = QRadioButton("自定义应用", self)
        radio_button1.setGeometry(10, 10, 100, 30)
        radio_button1.setChecked(True)
        radio_button2 = QRadioButton("应用商店", self)
        radio_button2.setGeometry(100, 10, 100, 30)
        radio_button1.show()
        radio_button2.show()

        # 设置 QRadioButton 的光标样式，使鼠标经过时变为指针
        radio_button1.setCursor(QCursor(Qt.PointingHandCursor))
        radio_button2.setCursor(QCursor(Qt.PointingHandCursor))

        # 创建按钮组来管理 QRadioButton
        button_group = QButtonGroup(self)
        button_group.addButton(radio_button1)
        button_group.addButton(radio_button2)

        # 连接信号和槽
        radio_button1.toggled.connect(self.show_list1)
        radio_button2.toggled.connect(self.show_list2)

        # 添加一个list
        self.app_list1 = QListWidget(self)
        self.app_list1.setGeometry(0, 40, APP_STORE_WIDTH - 10, self.size().height() - 40)

        self.app_list2 = QListWidget(self)
        self.app_list2.setGeometry(0, 40, APP_STORE_WIDTH - 10, self.size().height() - 40)

        self.spin_frame = SpinFrame(self)
        self.load_data()
        items2 = [
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
            (os.path.join(self.application_path, "images", "apk-icon.webp"), "Petco", "8.6.3"),
        ]

        for icon, name, version in items2:
            item2 = QListWidgetItem(self.app_list2)
            widget = AppItem(icon, name, version, '', parent.scrcpy_addr)
            item2.setSizeHint(widget.sizeHint())
            self.app_list2.setItemWidget(item2, widget)
        self.app_list1.show()
        self.app_list2.hide()

    @Slot()
    def load_data(self):
        # 创建并启动工作线程
        self.thread = WorkerThread(token=self.token,url='file/getAll')
        self.thread.data_fetched.connect(self.on_data_fetched)
        self.thread.start()

    @Slot()
    def on_data_fetched(self, data):
        self.app_list1.clear()

        filtered_apk_list = self.filter_apk_list(data)
        for icon, name, version, url in filtered_apk_list:
            item1 = QListWidgetItem(self.app_list1)
            widget = AppItem(icon, name, version, url, self.scrcpy_addr)
            item1.setSizeHint(widget.sizeHint())
            self.app_list1.setItemWidget(item1, widget)

        self.spin_frame.delete_spin()

    def filter_apk_list(self, params_list):
        """ 过滤所有apk文件 """
        temp_list = []
        if params_list:
            for li in params_list:
                if li.get('name').endswith('.apk'):
                    temp_list.append(li)

        temp_tulp_list = []
        for li in temp_list:
            path = os.path.join(self.application_path, 'images', 'apk-temp.png')
            name = li.get('name')
            version = li.get('version')
            apk_url = li.get('downloadUrl')
            temp_tulp_list.append((path, name, version, apk_url))

        return temp_tulp_list

    def show_list1(self):
        self.app_list1.show()
        self.app_list2.hide()

    def show_list2(self):
        self.app_list1.hide()
        self.app_list2.show()

    @staticmethod
    def run_adb_command(command):
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout, result.stderr

    def query_installed_apk(self):
        command = ["adb", "-s", self.scrcpy_addr, "shell", "pm", "list", "packages", "-f"]
        stdout, stderr = self.run_adb_command(command)
        if stderr:
            print(f"Error getting installed packages: {stderr}")
            return []

        packages = [line.split("=")[-1].strip() for line in stdout.splitlines()]
        paths = {line.split("=")[-1].strip(): line.split(":")[1].split("=")[0] for line in stdout.splitlines()}
        return packages, paths

    def get_app_name(self, package_name):
        command = ["adb", "-s", self.scrcpy_addr, "shell", "dumpsys", "package", package_name]
        stdout, stderr = self.run_adb_command(command)
        if stderr:
            print(f"Error getting app label for package {package_name}: {stderr}")
            return None

        label_match = re.search(r'ApplicationInfo.*?labelRes=(\S+)', stdout)
        if label_match:
            label_res = label_match.group(1)
            command = ["adb", "-s", self.scrcpy_addr, "shell", "pm", "dump", package_name]
            stdout, _ = self.run_adb_command(command)
            label = re.search(r'^\s*label=(.*)', stdout, re.MULTILINE)
            if label:
                return label.group(1)
        else:
            label_match = re.search(r'android:label="([^"]+)"', stdout)
        if label_match:
            return label_match.group(1)
        return package_name
