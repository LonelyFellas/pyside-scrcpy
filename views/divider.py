from PySide6.QtWidgets import QWidget, QFrame


class Divider(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(1)
        self.setStyleSheet("background-color: #f0f0f0;")


