from PySide6.QtGui import Qt, QMovie
from PySide6.QtWidgets import QLabel

from views.util import images_path


class SpinLabel(QLabel):
    def __init__(self, parent=None, width=50, height=50):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        x = (parent.width() - width) // 2
        y = (parent.height() - height) // 2
        self.setGeometry(x, y, width, height)

        print(parent.application_path)
        self.movie = QMovie(images_path(parent.application_path, 'loading.gif'))
        self.movie.setScaledSize(self.size())
        self.setMovie(self.movie)
        self.movie.start()

    def pause_movie(self):
        self.movie.stop()
        self.movie.deleteLater()
