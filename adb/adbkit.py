import subprocess
from typing import List, Optional, Literal

from views import handle_startupinfo


class Adbkit:
    def __init__(self, serial: str, is_init_connect: bool = True):
        super().__init__()
        self.serial = serial
        if is_init_connect:
            self.connect()

    def connect(self):
        subprocess.Popen(['adb', 'connect', self.serial], **handle_startupinfo())

    def disconnect(self):
        subprocess.Popen(['adb', 'disconnect', self.serial], **handle_startupinfo())

    def shell(self, command: List, run_type: Optional[Literal['run', 'popen', 'check_output']] = 'run'):
        base_command = ["adb", "-s", self.serial, "shell"]
        command = base_command + command

        if run_type == 'run':
            return subprocess.run(command, **handle_startupinfo())
        elif run_type == 'popen':
            return subprocess.Popen(command, **handle_startupinfo())
        else:
            output = subprocess.check_output(command, creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
            return output.decode('utf-8').strip()

    def query_system_orientation(self) -> int:
        """
        获取当前的屏幕是竖屏还是横屏 0，2为竖屏，1，3为横屏
        :return:
        """
        try:
            output = self.shell(
                ['settings', 'get', 'system', 'user_rotation'],
                run_type='check_output')
            return int(output)
        except Exception as e:
            print(f'Error: {e}')
            return 1

