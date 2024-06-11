from dataclasses import dataclass, field
from typing import Callable, Optional

from PySide6.QtWidgets import QMessageBox, QWidget
from PySide6.QtCore import QPoint


@dataclass
class ConfirmationParams:
    position: QPoint
    on_yes: Callable
    on_no: Callable
    title: Optional[str] = field(default="信息确认框")
    text: Optional[str] = field(default="你确定进行当前操作吗？")
    yes_text: Optional[str] = field(default="确定")
    no_text: Optional[str] = field(default="取消")


class ConfirmMsgBox(QMessageBox):
    def __init__(self, parent: QWidget, options: ConfirmationParams):
        super().__init__(parent)
        self.setWindowTitle(options.title)
        self.setText(options.text)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        yes_button = self.button(QMessageBox.Yes)
        no_button = self.button(QMessageBox.No)

        yes_button.setText(options.yes_text)
        no_button.setText(options.no_text)
        self.button(QMessageBox.Yes).clicked.connect(options.on_yes)
        self.button(QMessageBox.No).clicked.connect(options.on_no)

        self.move(options.position)
