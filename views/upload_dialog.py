import os

from PySide6.QtWidgets import QLabel, QListWidget, QListWidgetItem, QSizePolicy

from views.dialog import CustomDialogModal
from views.upload_progress_item import UploadProgressItem


class UploadDialog(CustomDialogModal):
    def __init__(self, parent=None, application_path=''):
        super().__init__(x=parent.x() + 10, y=105, width=520, height=310)
        self.application_path = application_path
        self.main_layout = self.setup_layout()
        self.items = []
        self.dialog.frame.setObjectName("upload_self_dialog")
        self.dialog.setStyleSheet(
            """
                QFrame#upload_self_dialog{
                    background-color: rgb(255, 255, 255); 
                    border-radius: 4px; 
                    padding: 10px;
                }
            """
        )
        title = QLabel("上传队列(2/2)")
        self.main_layout.addWidget(title)
        self.create_list_item()

    def create_list_item(self):
        self.files_list = QListWidget(self)
        self.files_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.get_list()
        self.main_layout.addWidget(self.files_list)

    def push_item(self, filename='', size=''):
        cover_path = os.path.join(self.application_path, 'images', 'flc-file-icon.png')
        self.items.append({'cover': cover_path, 'filename': filename, 'size': size})
        self.get_list('refresh')

    def get_list(self, get_type='init'):
        if get_type == 'update':
            self.files_list.clear()

        delete_icon_path = os.path.join(self.application_path, 'images', 'delete.png')
        for item in self.items:
            item_view = QListWidgetItem(self.files_list)
            item_widget = UploadProgressItem(item_view, item, delete_icon_path)
            item_view.setSizeHint(item_widget.sizeHint())
            self.files_list.setItemWidget(item_view, item_widget)

    def update_progress_value(self, index: int, value: int):
        if index < self.files_list.count():
            item_view = self.files_list.item(index)
            item_widget = self.files_list.itemWidget(item_view)
            item_widget.progress_widget.setValue(value)

    def super_show(self):
        self.show()

    def super_hide(self):
        self.hide()
