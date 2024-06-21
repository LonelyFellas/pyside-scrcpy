import os
from collections import deque

from PySide6.QtWidgets import QLabel, QListWidget, QListWidgetItem, QSizePolicy, QVBoxLayout

from global_state import GlobalState
from views.config import WIDTH_WINDOW
from views.dialog import CustomDialogModal
from views.empty import EmptyView
from views.upload_progress_item import UploadProgressItem


class UploadDialog(CustomDialogModal):
    def __init__(self, parent=None):
        super().__init__(x=parent.x() + WIDTH_WINDOW + 20, y=85, width=500, height=280)
        self.application_path = GlobalState().get_root_path()
        self.main_layout = None
        self.dq_items = deque()
        self.done_quantity = 0
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

    def setup_ui(self):
        self.main_layout = self.setup_layout()
        self.title = QLabel()
        self.modify_title(len(self.dq_items), self.done_quantity)
        self.main_layout.addWidget(self.title)
        self.empty_view = EmptyView(self.width() / 2, self.height() / 2 - 80, False, 50, 50, 14)
        self.main_layout.addWidget(self.empty_view)
        self.create_list_item()

    def modify_title(self, sum_quantity=0, done_quantity=0):
        self.title.setText(f"上传队列({done_quantity}/{sum_quantity})")

    def create_list_item(self):
        self.files_list = QListWidget(self)
        self.files_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.get_list()
        self.main_layout.addWidget(self.files_list)

    def push_item(self, filename='', size=''):
        cover_path = os.path.join(self.application_path, 'images', 'flc-file-icon.png')
        self.dq_items.appendleft({'cover': cover_path, 'filename': filename, 'size': size, 'is_done': False})
        self.get_list('update')
        self.modify_title(len(self.dq_items), self.done_quantity)

    def remove_item(self, item_views: QListWidgetItem, index: int):
        # 删除队列
        new_dq = deque()
        done_quantity = 0
        for i, item in enumerate(self.dq_items):
            if i != index:
                done_quantity += 1
                new_dq.append(item)
        self.done_quantity = done_quantity
        self.modify_title(len(new_dq), done_quantity)

        self.dq_items = new_dq

        # 然后删除ui
        row = self.files_list.row(item_views)
        self.files_list.takeItem(row)

        # 重新渲染ui
        self.get_list('update')

    def get_list(self, get_type='init'):
        if get_type == 'update':
            self.files_list.clear()

        delete_icon_path = os.path.join(self.application_path, 'images', 'delete.png')
        if len(self.dq_items) > 0:
            for index, item in enumerate(self.dq_items):
                item_view = QListWidgetItem(self.files_list)
                item_widget = UploadProgressItem(item_view, item, delete_icon_path, index)
                item_widget.remove_item_signal.connect(self.remove_item)
                item_view.setSizeHint(item_widget.sizeHint())
                self.files_list.setItemWidget(item_view, item_widget)
                self.files_list.show()
                self.empty_view.hide()
        else:
            self.files_list.hide()
            self.empty_view.show()

    def update_progress_value(self, value: int, filename: str):
        index = self.find_index_by_filename(filename)
        if index != -1:
            item_widget = self.find_item_widget(index)
            # 然后找到了ui控件，再去更新控件的状态值
            if item_widget is not None:
                if value == 100:
                    self.dq_items = self.update_at_index_value(index)
                    self.done_quantity += 1
                    self.modify_title(len(self.dq_items), self.done_quantity)
                    self.get_list('update')
                    item_widget.repaint()
                item_widget.progress_widget.setValue(value)

    def update_at_index_value(self, index):
        new_dq = deque()
        for i, item in enumerate(self.dq_items):
            if i == index:
                new_dict = self.dq_items[index]
                new_dict["is_done"] = True
                new_dq.append(new_dict)
            else:
                new_dq.append(item)
        return new_dq

    def update_speed_value(self, speed: int, filename: str):
        index = self.find_index_by_filename(filename)
        if index != -1:
            item_widget = self.find_item_widget(index)
            # 然后找到了ui控件，再去更新控件的状态值
            if item_widget is not None:
                if speed == -1:
                    speed_str = ''
                elif speed < 1024:
                    speed_str = f"({speed:.2f}KB/s)"
                else:
                    speed_str = f"({speed / 1024:.2f}MB/s)"
                item_widget.speed_label.setText('' if speed == '' else speed_str)

    def find_item_widget(self, index: int):
        """
        得到索引值，再找到要更新的ui控件
        :param index:
        :return:
        """
        if index < self.files_list.count():
            item_view = self.files_list.item(index)
            item_widget = self.files_list.itemWidget(item_view)
            return item_widget
        return None

    def find_index_by_filename(self, filename):
        """
        通过文件名找到当前是要更新的索引值
        :param filename:
        :return:
        """
        for index, item in enumerate(self.dq_items):
            if item.get('filename') == filename:
                return index
        return -1

    def super_show(self):
        self.dialog.open()
        self.show()

    def super_hide(self):
        self.dialog.close()
        self.hide()
