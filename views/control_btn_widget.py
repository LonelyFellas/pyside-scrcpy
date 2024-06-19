from typing import Dict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QGraphicsOpacityEffect

from views.config import WIDTH_WINDOW, SCRCPY_WIDTH
from views.util import img_label


class ControlBtnWidget(QFrame):
    def __init__(self, parent=None, btn=None):
        super().__init__(parent)
        if btn is None:
            btn = {}
        self.btn = btn
        self.setFixedSize(WIDTH_WINDOW - SCRCPY_WIDTH, 35)
        self.setObjectName('control_btn')
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
        if event.button() == Qt.LeftButton:
            self.opacity_effect = QGraphicsOpacityEffect()
            self.setGraphicsEffect(self.opacity_effect)
            self.opacity_effect.setOpacity(0.7)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.rect().contains(event.pos()):
                # 触发点击事件
                if self.btn.get('on_click') is not None:
                    self.btn.get('on_click')()

                self.opacity_effect = QGraphicsOpacityEffect()
                self.setGraphicsEffect(self.opacity_effect)
                self.opacity_effect.setOpacity(1)
        super().mouseReleaseEvent(event)
