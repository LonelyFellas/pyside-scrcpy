from adb import Adbkit


class GlobalState:
    _instance = None
    _token = ''  # token
    _env_id = -1  # 环境Id
    _root_path = ''  # 当前路径
    _is_vertical_screen = ''  # 当前是否是竖屏
    _orientation = -1  # 方向号 0, 2 -> 竖屏 1, 3 -> 横屏
    _device = None
    _window_size = 'default'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalState, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self, token='', env_id=-1, root_path='', is_vertical_screen=False, orientation=-1, device=None,
             window_size='default'):
        self._token = token
        self._env_id = env_id
        self._root_path = root_path
        self._is_vertical_screen = is_vertical_screen
        self._orientation = orientation
        self._device = device
        self._window_size = window_size

    def get_device(self) -> Adbkit:
        return self._device

    def get_token(self):
        return self._token

    def get_env_id(self):
        return self._env_id

    def get_root_path(self):
        return self._root_path

    def get_window_size(self):
        return self._size

    def get_orientation(self):
        return self._orientation

    def set_orientation(self, orientation):
        self._orientation = orientation

    def get_is_vertical_screen(self):
        return self._is_vertical_screen

    def set_is_vertical_screen(self, value):
        self._is_vertical_screen = value
