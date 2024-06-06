import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget


def images_path(app_path, path=''):
    return os.path.join(app_path, 'images', path)


def view_cursor(widget: QWidget):
    widget.setCursor(QCursor(Qt.PointingHandCursor))
