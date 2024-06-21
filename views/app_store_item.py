import subprocess

from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QSizePolicy


class AppItem(QWidget):
    def __init__(self, icon_path, name, version, url, scrcpy_addr=''):
        super().__init__()
        self.url = url
        self.scrcpy_addr = scrcpy_addr

        layout = QHBoxLayout()

        # Icon
        icon_label = QLabel()
        icon_pixmap = QPixmap(icon_path).scaled(50, 50, aspectMode=Qt.KeepAspectRatio)
        icon_label.setPixmap(icon_pixmap)
        layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)  # 设置水平方向扩展
        text_layout.addWidget(left_spacer)
        _name = name if len(name) <= 40 else f'{name[:40]}...'
        name_label = QLabel(_name)
        name_label.setToolTip(name)
        version_label = QLabel(version)
        text_layout.addWidget(name_label)
        text_layout.addWidget(version_label)
        layout.addLayout(text_layout)

        # Install Button
        install_button = QPushButton("安装")
        install_button.setFixedSize(60, 30)
        layout.addWidget(install_button)
        install_button.clicked.connect(self.install_apk)

        self.setLayout(layout)

    @staticmethod
    def run_adb_command(command):
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout, result.stderr

    def install_apk(self):
        command = ["adb", "-s", self.scrcpy_addr, "shell", "pm", "list", "packages"]
    #     stdout, stderr = self.run_adb_command(command)
    #     if stderr:
    #         print(f"Error getting installed packages: {stderr}")
    #         return []
    #
    #     packages = [line.split(":")[1].strip() for line in stdout.splitlines()]
    #
    #     app_names = []
    #     for package in packages:
    #         app_name = self.get_app_name(package)
    #         app_names.append(app_name)
    #
    #     # print(app_names)
    #
    # def get_app_name(self, package_name):
    #     command = ["adb", "-s", self.scrcpy_addr, "shell", "dumpsys", "package", package_name]
    #     stdout, stderr = self.run_adb_command(command)
    #     if stderr:
    #         print(f"Error getting app name for package {package_name}: {stderr}")
    #         return None
    #
    #     for line in stdout.splitlines():
    #         if "ApplicationInfo" in line and "labelRes" in line:
    #             label_res = line.split("labelRes=")[1].split()[0]
    #             if label_res.isdigit():
    #                 command = ["adb", "-s", self, "shell", "pm", "dump", package_name, "|", "grep", "labelRes"]
    #                 stdout, _ = self.run_adb_command(command)
    #             if stdout:
    #                 return stdout.split("=")[1].strip()
    #             break
    #         elif "android:name" in line:
    #             return line.split("=")[1].strip()
    #     return package_name
    #     # # 获取安装输出
    #     # output, error = process.()
    #     # output_str = output.decode('utf-8')
    #     #
    #     # # 查找进度信息
    #     # progress_match = re.search(r"(\d+)%", output_str)
    #     #
    #     # progress = None
    #     # if progress_match:
    #     #     progress = int(progress_match.group(1))
    #     # else:
    #     #     # 如果没有找到进度信息，则可能发生错误
    #     #     print(f"安装 APK 时发生错误：{error}")
    #     #
    #     # if progress is not None:
    #     #     print(f"安装进度：{progress}%")
    #     # else:
    #     #     print("安装失败")
    #
    #
