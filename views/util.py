import os

from PySide6 import QtGui
from PySide6.QtCore import Qt, Signal, QObject, Property
from PySide6.QtGui import QCursor, QPixmap
from PySide6.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QLabel

from global_state import GlobalState


def images_path(app_path, path=''):
    return os.path.join(app_path, 'images', path)


# 将控件的鼠标样式设置为Pointer
def view_cursor(widget: QWidget, cursor: QCursor = Qt.PointingHandCursor):
    widget.setCursor(QCursor(cursor))


# 将控件设置背景颜色
def palette_bg_color(widget: QWidget, color='red'):
    # 创建一个QPalette对象
    palette = widget.palette()
    # 设置背景颜色
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
    # 应用调色板
    widget.setPalette(palette)
    # 确保自动填充背景
    widget.setAutoFillBackground(True)


# 间距控件
def spacer_item(width=10, height=10):
    return QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)


# 图片控件
def img_label(width=0, height=0, btn_path=''):
    btn_icon = QLabel()
    pixmap = QPixmap(images_path(GlobalState().get_root_path(), btn_path))  # 替换为你的图片路径
    pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    btn_icon.setPixmap(pixmap)
    return btn_icon


class StateObject(QObject):
    valueChanged = Signal(object)

    def __init__(self, init_value):
        super().__init__()
        self._value = init_value

    def get_value(self):
        return self._value

    def set_value(self, value):
        if self._value != value:
            self._value = value
            self.valueChanged.emit(value)

    value = Property(object, get_value, set_value, notify=valueChanged)
