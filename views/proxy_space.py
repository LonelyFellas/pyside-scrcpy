import os

from PySide6.QtCore import QSize, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QPushButton, QWidget, QHBoxLayout, QLabel, QTableWidget, \
    QHeaderView, QVBoxLayout

from views.config import PROXY_WIDTH
from views.util import view_cursor


class ProxySpace(QFrame):
    def __init__(self, parent=None, width_window=0, application_path='', token=''):
        super().__init__(parent)
        self.setGeometry(width_window, 10, PROXY_WIDTH - 10, parent.size().height() - 20)
        self.token = token
        self.application_path = application_path

        self.top_layout = None
        self.bottom_layout = None

        self.setObjectName("proxy_space_frame")
        self.setStyleSheet("#proxy_space_frame { border: 1px solid gray; background-color: white; }")

        self.main_layout = QVBoxLayout()

        # Top part with IP address, status and type
        self.create_top_widget()

        self.main_layout.addSpacing(20)

        # Table
        table = QTableWidget(2, 3)
        table.setFixedSize(420, 565)

        table.setHorizontalHeaderLabels(["代理信息", "代理账号", "操作"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setCellWidget(0, 0, QLabel("socks5://1:1"))
        table.setCellWidget(0, 1, QLabel("1"))
        table.setCellWidget(0, 2, self.create_operations_widget())

        table.setCellWidget(1, 0, QLabel("socks5://2222:1"))
        table.setCellWidget(1, 1, QLabel("1"))
        table.setCellWidget(1, 2, self.create_operations_widget())

        # 将表格添加到主layout里面去
        self.main_layout.addWidget(table)

        # 将分页添加到主layout里面去
        self.create_pagination_widget()

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
            QPushButton#switch_operate_btn {
                background-color: rgb(30, 77, 255); 
                color: white;
                border-radius: 2px;
            }
            QPushButton#switch_operate_btn:hover {
                background-color: rgb(15, 50, 255); 
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
            QPushButton#outline_btn_none {
                border: none;
                outline: none;
            }
            QPushButton#outline_btn_none:hover {
                background-color: #eee; 
                border-radius: 2px;
            }
            QPushButton#outline_btn_none:pressed {
                background-color: #ccc;
            }
            
            #proxy_space_frame { 
                border: 1px solid gray; background-color: white; 
            }
            
            QHeaderView::section:horizontal {
                border: 1px solid gray;
            }
            QTableCornerButton::section {
                border: none;  /* 移除表头左上角的边框 */
            }
            
        """)

    # @Slot()
    # def load_data(self):
    #     self.
    def create_top_widget(self):
        self.top_layout = QHBoxLayout()
        top_left_layout = QVBoxLayout()
        top_left_second_layout = QHBoxLayout()

        # top left
        ip_label = QLabel("IP地址：socks5://1:1@22222:1")
        start_status_label = QLabel("启动状态：已启动")
        proxy_type_label = QLabel("代理类型：socks5")
        top_left_second_layout.addWidget(start_status_label)
        top_left_second_layout.addSpacing(20)  # 增加固定大小的空白
        top_left_second_layout.addWidget(proxy_type_label)
        top_left_layout.addWidget(ip_label)
        top_left_layout.addSpacing(10)
        top_left_layout.addLayout(top_left_second_layout)

        # top right
        clear_button = QPushButton("清空当前代理")
        clear_button.setObjectName("clear_proxy_btn")

        view_cursor(clear_button)
        self.top_layout.addLayout(top_left_layout)
        self.top_layout.addStretch()
        self.top_layout.addWidget(clear_button)
        self.main_layout.addLayout(self.top_layout)

    def create_pagination_widget(self):
        self.bottom_layout = QHBoxLayout()

        total_label = QLabel("总数：2")
        page_label = QLabel("1")

        prev_button = QPushButton()
        prev_button.setIcon(QIcon(os.path.join(self.application_path, 'images', 'prev_page.png')))
        prev_button.setObjectName("outline_btn_none")
        prev_button.setIconSize(QSize(24, 24))
        view_cursor(prev_button)
        next_button = QPushButton()
        next_button.setIcon(QIcon(os.path.join(self.application_path, 'images', 'next_page.png')))
        next_button.setObjectName("outline_btn_none")
        next_button.setIconSize(QSize(24, 24))
        view_cursor(next_button)

        page_layout = QHBoxLayout()
        page_layout.addWidget(total_label)
        page_layout.addStretch()
        page_layout.addWidget(prev_button)
        page_layout.addWidget(page_label)
        page_layout.addWidget(next_button)

        self.bottom_layout.addLayout(page_layout)

        per_page_label = QLabel("10条/页")
        self.bottom_layout.addWidget(per_page_label)
        self.main_layout.addLayout(self.bottom_layout)

    @staticmethod
    def create_operations_widget():
        widget = QWidget()
        layout = QHBoxLayout()
        switch_button = QPushButton("切换")
        switch_button.setFixedSize(50, 20)
        delete_button = QPushButton("删除")
        delete_button.setFixedSize(50, 20)
        layout.addWidget(switch_button)
        layout.addWidget(delete_button)
        switch_button.setObjectName("switch_operate_btn")
        delete_button.setObjectName("delete_operate_btn")
        view_cursor(delete_button)
        view_cursor(switch_button)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        return widget
