from PySide6.QtGui import Qt, QMovie
from PySide6.QtWidgets import QLabel, QFrame

from global_state import GlobalState
from views.util import images_path


class SpinFrame(QFrame):
    def __init__(self, parent=None, width=50, height=50):
        super().__init__(parent)
        self.application_path = GlobalState().get_root_path()
        self.setFixedSize(parent.size())
        self.setStyleSheet("background-color: rgba(255,255,255,0.4);")
        self._label_width = width
        self._label_width = height
        self.spin_label = SpinLabel(self)
        self.raise_()

    def delete_spin(self):
        self.spin_label.delete_spin()
        self.deleteLater()

    def hide_spin(self):
        self.spin_label.hide_spin()
        self.hide()

    def show_spin(self):
        self.show()
        self.spin_label.movie.start()
        self.spin_label.show()


class SpinLabel(QLabel):
    def __init__(self, parent=None, width=50, height=50):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        x = (parent.width() - width) // 2
        y = (parent.height() - height) // 2
        self.setGeometry(x, y, width, height)
        self.movie = QMovie(images_path(parent.application_path, 'loading.gif'))
        self.movie.setScaledSize(self.size())
        self.setMovie(self.movie)
        self.raise_()
        self.movie.start()

    def delete_spin(self):
        self.movie.stop()
        self.movie.deleteLater()

    def hide_spin(self):
        self.movie.stop()
        self.hide()
