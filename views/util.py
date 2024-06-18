import os

from PySide6.QtCore import Qt, Signal, QObject, Property
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget


def images_path(app_path, path=''):
    return os.path.join(app_path, 'images', path)


def view_cursor(widget: QWidget):
    widget.setCursor(QCursor(Qt.PointingHandCursor))


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
