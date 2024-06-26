from functools import partial
from typing import Optional, Literal, List

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFrame, QPushButton, QWidget, QHBoxLayout, QLabel, QTableWidget, \
    QHeaderView, QVBoxLayout

from global_state import GlobalState
from views.config import EXPEND_WIDTH, HEIGHT_WINDOW
from views.confirm_msg_box import ConfirmationParams, ConfirmMsgBox
from views.pagination_widget import PaginationWidget
from views.spin_label import SpinFrame
from views.util import view_cursor
from views.worker_thread import WorkerThread

PROXY_MAPPING = {
    1: 'socks5',
    2: 'http',
    3: 'https'
}


class ProxySpace(QFrame):
    def __init__(self, parent=None, height=0):
        super().__init__(parent)
        self.setFixedSize(EXPEND_WIDTH, height)
        self.token = GlobalState().token
        self.env_id = GlobalState().env_id
        self.application_path = GlobalState().root_path
        self.pageNo = 1
        self.pageSize = 20
        self.data = []
        self.top_layout = None
        self.bottom_layout = None
        self.done_thread = 0

        self.setObjectName("proxy_space_frame")
        self.setStyleSheet("#proxy_space_frame { border: 1px solid gray; background-color: white; }")

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(10, 10, 10, 0)

        # Top part with IP address, status and type
        self.create_top_widget()

        self.main_layout.addSpacing(10)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setContentsMargins(0, 0, 0, 0)
        self.table.setFixedSize(520, 513)

        self.table.setHorizontalHeaderLabels(["代理信息", "代理账号", "操作"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 将表格添加到主layout里面去
        self.main_layout.addWidget(self.table)
        self.pagination = PaginationWidget(0, self.pageNo, self.pageSize, 0)
        self.pagination.prev_signal.connect(lambda: self.page_changed('prev'))
        self.pagination.next_signal.connect(lambda: self.page_changed('next'))
        self.main_layout.addWidget(self.pagination)

        container = QWidget(self)
        container.setLayout(self.main_layout)

        self.setStyleSheet("""
            QPushButton#clear_proxy_btn {
                padding: 6px;
                border-radius: 3px;
                background-color: rgb(255, 77, 79);
                color: white;
            }
            QPushButton#clear_proxy_btn:hover {
                background-color: rgb(255, 55, 58);
            }
            QPushButton#clear_proxy_btn:pressed{
                background-color: rgb(255, 33, 33);
            }
            QPushButton#switch_operate_btn {
                background-color: rgb(30, 77, 255); 
                color: white;
                border-radius: 2px;
            }
            QPushButton#switch_operate_btn:hover {
                background-color: rgb(15, 50, 255); 
            }
            QPushButton#switch_operate_btn:pressed{
                background-color: rgb(0, 30, 255);
            }
            QPushButton#delete_operate_btn {
                color: rgb(255, 77, 79);
                outline: none; 
                border: none;
            }
            QPushButton#delete_operate_btn:hover {
                color: rgb(255, 55, 58);
                border-radius: 2px;
                background-color: #eee; 
            }
            QPushButton#delete_operate_btn:pressed {
                color: rgb(255, 33, 55);
                border-radius: 2px;
                background-color: #ccc;
            }
            #proxy_space_frame { 
                border: 1px solid gray; background-color: white; 
            }
            QHeaderView::section:horizontal {
                border: 1px solid gray;
            }
        """)
        self.spin_frame = SpinFrame(self)
        self.load_data()

    def page_changed(self, page_type: Optional[Literal['prev', 'next']]):
        self.pageNo += (1 if page_type == 'next' else -1)
        self.update_list()

    @Slot()
    def load_data(self):
        self.thread_env_detail = WorkerThread(token=self.token, url='env/getCurrentVpc', data={'envId': self.env_id},
                                              option={"method": 'post'})
        self.thread_vpc_list = WorkerThread(token=self.token, url='vpc/getAll')
        self.thread_env_detail.data_fetched.connect(lambda data: self.on_data_fetched(data, 'env_detail'))
        self.thread_vpc_list.data_fetched.connect(lambda data: self.on_data_fetched(data, 'vpc_list'))
        self.thread_vpc_list.start()
        self.thread_env_detail.start()

    @Slot(object, str)
    def on_data_fetched(self, data, fetched_type):
        self.done_thread += 1

        if fetched_type == 'env_detail':
            addr = data['addr'] if 'addr' in data else '暂无'
            proxy_type = PROXY_MAPPING.get(data['type']) if 'type' in data else '暂无'
            status_type = data['statusText'] if 'statusText' in data else '暂无'
            self.update_top_view(addr, status_type, proxy_type)
        if fetched_type == 'vpc_list':
            self.data = data
            len_data = len(data)
            self.pagination.set_option(option={
                "page_sum": len_data,
            })
            self.update_list()

        if self.done_thread == 2:
            self.spin_frame.hide_spin()

    def update_list(self):
        gap = len(self.data) - (self.pageNo - 1) * self.pageSize
        current_quantity = 20 if gap >= 20 else gap
        self.table.setRowCount(current_quantity)
        self.pagination.set_sum_item(current_quantity)
        for index, item in enumerate(self.data[((self.pageNo - 1) * self.pageSize): (self.pageNo * self.pageSize)]):
            proxy_info = f'{PROXY_MAPPING.get(item['type'])}://{item['address']}:{item['port']}'
            self.table.setCellWidget(index, 0, self.create_cell_widget(QLabel(proxy_info)))
            self.table.setCellWidget(index, 1, self.create_cell_widget(QLabel(item['username'])))
            self.table.setCellWidget(index, 2, self.create_operations_widget(item['id']))

    def update_top_view(self, addr='', status_text='', type=''):
        self.ip_label.setText(f"IP地址：{addr}")
        self.start_status_label.setText(f"启动状态：{status_text}")
        self.proxy_type_label.setText(f"代理类型：{type}")

    def create_top_widget(self):
        self.top_layout = QHBoxLayout()
        top_left_layout = QVBoxLayout()
        top_left_second_layout = QHBoxLayout()

        # top left
        self.ip_label = QLabel(f"IP地址：暂无")
        self.start_status_label = QLabel(f"启动状态：未启动")
        self.proxy_type_label = QLabel(f"代理类型：socks")
        top_left_second_layout.addWidget(self.start_status_label)
        top_left_second_layout.addSpacing(20)  # 增加固定大小的空白
        top_left_second_layout.addWidget(self.proxy_type_label)
        top_left_layout.addWidget(self.ip_label)
        top_left_layout.addSpacing(10)
        top_left_layout.addLayout(top_left_second_layout)

        # top right
        self.clear_button = QPushButton("清空当前代理")
        self.clear_button.setObjectName("clear_proxy_btn")
        self.clear_button.clicked.connect(self.handle_clear_proxy)

        view_cursor(self.clear_button)
        self.top_layout.addLayout(top_left_layout)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.clear_button)
        self.main_layout.addLayout(self.top_layout)

    @Slot()
    def handle_clear_proxy(self):
        button_position = self.clear_button.mapToGlobal(self.clear_button.rect().center())
        message_box = ConfirmMsgBox(self,
                                    ConfirmationParams(position=button_position, on_yes=self.handle_clear_proxy_yes,
                                                       on_no=self.handle_clear_proxy_no, title="清除代理",
                                                       text="你确定是否清除当前代理"))
        message_box.exec_()

    @Slot()
    def handle_clear_proxy_yes(self):
        self.spin_frame.show_spin()
        self.thread_clear_proxy = WorkerThread(token=self.token, url='env/clearVpc', data={'envId': self.env_id},
                                               option={"method": "post"})
        self.thread_clear_proxy.data_fetched.connect(self.refresh_env_detail)
        self.thread_clear_proxy.start()

    @Slot()
    def refresh_env_detail(self):
        self.thread_env_detail = WorkerThread(token=self.token, url='env/getCurrentVpc', data={'envId': self.env_id},
                                              option={"method": 'post'})
        self.thread_env_detail.data_fetched.connect(self.refreshed_env_detail)
        self.thread_env_detail.start()

    @Slot()
    def refreshed_env_detail(self, data):
        addr = data['addr'] if 'addr' in data else '暂无'
        proxy_type = PROXY_MAPPING.get(data['type']) if 'type' in data else '暂无'
        status_type = data['status_type'] if 'status_type' in data else '暂无'
        self.update_top_view(addr, status_type, proxy_type)
        self.spin_frame.hide_spin()

    @Slot()
    def handle_clear_proxy_no(self):
        print("No clicked!")

    # def create_pagination_widget(self):

    def create_operations_widget(self, vpc_id: int):
        widget = QWidget()
        layout = QHBoxLayout()
        switch_button = QPushButton("切换")
        switch_button.setFixedSize(50, 20)
        switch_button.clicked.connect(partial(self.handle_switch_proxy_btn, vpc_id))
        delete_button = QPushButton("删除")
        delete_button.setFixedSize(50, 20)
        delete_button.clicked.connect(partial(self.handle_delete_proxy_btn, vpc_id, delete_button))
        layout.addWidget(switch_button)
        layout.addWidget(delete_button)
        switch_button.setObjectName("switch_operate_btn")
        delete_button.setObjectName("delete_operate_btn")
        view_cursor(delete_button)
        view_cursor(switch_button)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        return widget

    @Slot()
    def handle_switch_proxy_btn(self, vpc_id):
        self.spin_frame.show_spin()
        self.thread_switch_proxy = WorkerThread(token=self.token, url='env/setVpc', data={
            'envId': self.env_id,
            'vpcId': vpc_id
        }, option={"method": "post"})

        self.thread_switch_proxy.data_fetched.connect(self.refresh_env_detail)
        self.thread_switch_proxy.start()

    @Slot()
    def handle_delete_proxy_btn(self, vpc_id, delete_btn: QPushButton):
        button_position = delete_btn.mapToGlobal(delete_btn.rect().center())
        message_box = ConfirmMsgBox(self,
                                    ConfirmationParams(position=button_position,
                                                       on_yes=partial(self.handle_delete_proxy_yes, vpc_id),
                                                       on_no=self.handle_clear_proxy_no, title="删除代理",
                                                       text="你确定是否删除代理"))
        message_box.exec_()

    @Slot()
    def handle_delete_proxy_yes(self, vpc_id):
        self.spin_frame.show_spin()
        self.thread_delete_vpc_list = WorkerThread(token=self.token, url='vpc/delete', data={"id": vpc_id},
                                                   option={"method": "post"})
        self.thread_delete_vpc_list.data_fetched.connect(self.refresh_vpc_list)
        self.thread_delete_vpc_list.start()

    @Slot()
    def refresh_vpc_list(self):
        self.spin_frame.show_spin()
        self.thread_vpc_list = WorkerThread(token=self.token, url='vpc/getAll')
        self.thread_vpc_list.data_fetched.connect(self.refreshed_vpc_list)
        self.thread_vpc_list.start()

    @Slot()
    def refreshed_vpc_list(self, data):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(3)
        self.pagination.set_sum_item(len(data))
        for index, item in enumerate(data):
            proxy_info = f'{PROXY_MAPPING.get(item['type'])}://{item['address']}:{item['port']}'
            self.table.setCellWidget(index, 0, self.create_cell_widget(QLabel(proxy_info)))
            self.table.setCellWidget(index, 1, self.create_cell_widget(QLabel(item['username'])))
            self.table.setCellWidget(index, 2, self.create_operations_widget(item['id']))
        self.spin_frame.hide_spin()

    @staticmethod
    def create_cell_widget(widget: QWidget):
        container = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(widget)
        layout.setContentsMargins(5, 5, 5, 5)  # 设置边距
        container.setLayout(layout)
        return container
