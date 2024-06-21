from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QGraphicsOpacityEffect

from views.config import WIDTH_WINDOW, SCRCPY_WIDTH
from views.util import img_label, view_cursor


class ControlBtnWidget(QFrame):
    def __init__(self, parent=None, btn=None):
        super().__init__(parent)
        if btn is None:
            btn = {}
        self.btn = btn
        self.setFixedSize(WIDTH_WINDOW - SCRCPY_WIDTH, 35)
        if btn['on_click'] is None:
            self.opacity_effect = QGraphicsOpacityEffect()
            self.setGraphicsEffect(self.opacity_effect)
            self.opacity_effect.setOpacity(0.3)
        else:
            self.setObjectName('control_btn')
            view_cursor(self)
        self.setMouseTracking(True)  # 启用鼠标跟踪

        btn_layout = QVBoxLayout(self)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(0)

        btn_icon = img_label(width=18, height=18, btn_path=btn['icon'])
        btn_icon.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(btn_icon)

        if btn.get('title'):
            btn_title = QLabel(btn.get('title'))
            btn_title.setAlignment(Qt.AlignCenter)
            btn_layout.addWidget(btn_title)

        self.setStyleSheet("""
            QFrame#control_btn {
                background-color: transparent;
                outline: none;
                border: 1px solid transparent; /* 初始状态的边框颜色 */
            }
            QFrame#control_btn:hover {
                background-color: rgb(255, 255, 255);
                border: 1px solid gray; /* hover 状态的边框颜色 */
            }
            QFrame#control_btn_press {
                background-color: rgb(199, 200, 200);
                outline: none;
                border: 1px solid gray; /* pressed 状态的边框颜色 */
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.btn['on_click'] is not None:
            self.opacity_effect = QGraphicsOpacityEffect()
            self.setGraphicsEffect(self.opacity_effect)
            self.opacity_effect.setOpacity(0.7)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.btn['on_click'] is not None:
            if self.rect().contains(event.pos()):
                self.opacity_effect = QGraphicsOpacityEffect()
                self.setGraphicsEffect(self.opacity_effect)
                self.opacity_effect.setOpacity(1)

                # 为什么把是super在这里执行呢，因为onclick执行了delete操作，同步操作导致后面super堆内存被删除，控制台报异常
                super().mouseReleaseEvent(event)
                # 触发点击事件
                if self.btn.get('on_click') is not None:
                    self.btn.get('on_click')()
                    return

        super().mouseReleaseEvent(event)
