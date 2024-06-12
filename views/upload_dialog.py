from PySide6.QtWidgets import QLabel

from views.dialog import CustomDialogModal


class UploadDialog(CustomDialogModal):
    def __init__(self, parent=None):
        super().__init__(x=parent.x() + 10, y=90, width=520, height=50)
        main_layout = self.setup_layout()
        label = QLabel("上传文件的历史记录")
        label.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); border-radius: 4px;")
        main_layout.addWidget(label)
