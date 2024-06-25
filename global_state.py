from typing import Tuple

from adb import Adbkit


class GlobalState:
    _instance = None
    _token = ''  # token
    _env_id = -1  # 环境Id
    _root_path = ''  # 当前路径
    _is_vertical_screen = ''  # 当前是否是竖屏
    _orientation = -1  # 方向号 0, 2 -> 竖屏 1, 3 -> 横屏
    _device = None
    # SCRCPY_WIDTH, SCRCPY_HEIGHT
    _sizes = (0, 0)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalState, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self, token='', env_id=-1, root_path='', is_vertical_screen=False, orientation=-1, device=None,
             sizes=(0, 0)):
        self._token = token
        self._env_id = env_id
        self._root_path = root_path
        self._is_vertical_screen = is_vertical_screen
        self._orientation = orientation
        self._device = device
        self.sizes = sizes

    @property
    def device(self) -> Adbkit:
        return self._device

    @property
    def token(self):
        return self._token

    @property
    def env_id(self):
        return self._env_id

    @property
    def root_path(self):
        return self._root_path

    @property
    def sizes(self):
        return self._sizes

    @sizes.setter
    def sizes(self, s: Tuple[int, int]):
        self._sizes = s

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        self._orientation = orientation

    @property
    def is_vertical_screen(self):
        return self._is_vertical_screen

    @is_vertical_screen.setter
    def is_vertical_screen(self, value: bool):
        self._is_vertical_screen = value

    def revert_size(self):
        self.sizes = (self._sizes[1], self._sizes[0])
