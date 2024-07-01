from PySide6.QtWidgets import QFrame

from views.util import palette_bg_color


class UploadTransSpace(QFrame):
    def __init__(self):
        super().__init__()
        palette_bg_color(self, 'yellow')
