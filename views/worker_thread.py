import requests
from PySide6.QtCore import QThread, Signal

from views.config import API_URL


class WorkerThread(QThread):
    data_fetched = Signal(list)  # 定义一个信号，用于传递获取的数据

    def __init__(self, token, url):
        super().__init__()
        self.token = token
        self.url = API_URL + url

    def run(self):
        """ 查询我中转站上传的所有文件 """
        res_list = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-type': 'application/json',
            'X-Token': self.token
        }

        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            res_list = response.json().get('data')
        else:
            res_list: []

        print(res_list)
        self.data_fetched.emit(res_list)  # 发射信号传递数据
