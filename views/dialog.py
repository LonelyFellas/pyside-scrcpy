from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QDialog, QFrame, QGraphicsDropShadowEffect, QVBoxLayout, QLabel


class CustomDialogModal(QFrame):
    def __init__(self, parent=None, x=0, y=0, width=200, height=100):
        super().__init__(parent)
        self.setGeometry(0, 0, 1020, 702)
        self.dialog = CustomDialog(self)
        self.dialog.setGeometry(x, y, width, height)
        self.dialog.show()
        self.installEventFilter(self)

    def setup_layout(self):
        return self.dialog.main_layout

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if not self.dialog.geometry().contains(event.pos()):
                self.dialog.close()
                self.hide()
                return True
        return super().eventFilter(obj, event)


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置窗口标题
        self.setWindowTitle('Upload Dialog')
        # 设置对话框为无边框模式和弹出模式
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgb(255,255,255);")

        self.setAttribute(Qt.WA_TranslucentBackground)

        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(4)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(Qt.black)

        # 设置阴影效果到对话框
        self.setGraphicsEffect(shadow)
        # 创建主布局

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)  # 添加边距以显示阴影效果
        # 设置主布局
        self.setLayout(self.main_layout)
