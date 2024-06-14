from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QDialog, QFrame, QGraphicsDropShadowEffect, QVBoxLayout, QLabel


class CustomDialogModal(QFrame):
    def __init__(self, x=0, y=0, width=200, height=100):
        super().__init__()
        self.setGeometry(0, 0, 1020, 702)
        self.dialog = CustomDialog(self, x, y, width, height)
        self.installEventFilter(self)

    def setup_layout(self):
        return self.dialog.main_layout

    def set_layout_style(self, style: str):
        return self.dialog.frame.setStyleSheet(style)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if not self.dialog.geometry().contains(event.pos()):
                self.dialog.close()
                self.hide()
                return True
        return super().eventFilter(obj, event)


class CustomDialog(QDialog):
    def __init__(self, parent=None, x=0, y=0, width=200, height=100):
        super().__init__(parent)
        # 设置窗口标题
        self.setWindowTitle('Upload Dialog')
        # 设置对话框为无边框模式和弹出模式
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(x, y, width, height)

        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(4)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(Qt.black)

        # 设置阴影效果到对话框
        self.setGraphicsEffect(shadow)
        # 创建主布局

        self.frame = QFrame(self)
        self.frame.resize(self.size())
        self.main_layout = QVBoxLayout(self.frame)
        self.main_layout.setContentsMargins(10, 10, 10, 10)  # 添加边距以显示阴影效果
        # 设置主布局
        self.setLayout(self.main_layout)
