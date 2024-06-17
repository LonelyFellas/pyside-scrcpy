import os
import subprocess
import time

from PySide6.QtCore import QThread, Signal

from views import handle_startupinfo


class AdbPushThread(QThread):
    progress_signal = Signal(int, str)
    speed_signal = Signal(float, str)
    message_signal = Signal(str, str)

    def __init__(self, serial, local_path, remote_path, filename):
        super().__init__()
        self.filename = filename
        self.serial = serial
        self.local_path = local_path
        self.remote_path = remote_path

    def run(self):
        if not os.path.exists(self.local_path):
            self.message_signal.emit(f"Error: File does not exist: {self.local_path}", self.filename)
            return

        file_size = os.path.getsize(self.local_path)
        if file_size == 0:
            self.message_signal.emit("Error: File size is 0. Please check the file path and ensure the file exists.",
                                     self.filename)
            return

        self.message_signal.emit(f"File size: {file_size} bytes", self.filename)
        pushed_bytes = 0

        adb_command = ["adb", "-s", self.serial, "push", self.local_path, self.remote_path]
        process = subprocess.Popen(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   encoding='utf-8')

        start_time = time.time()

        while process.poll() is None:
            result = subprocess.run(["adb", "-s", self.serial, "shell", f"stat -c%s {self.remote_path}"],
                                    capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                try:
                    pushed_bytes = int(result.stdout.strip())
                    progress = int((pushed_bytes / file_size) * 100)
                    elapsed_time = time.time() - start_time
                    speed = pushed_bytes / elapsed_time
                    self.progress_signal.emit(progress, self.filename)
                    self.speed_signal.emit(speed / 1024, self.filename)
                except ValueError:
                    self.message_signal.emit(f"Error parsing file size: {result.stdout.strip()}", self.filename)

            time.sleep(1)

        process.wait()

        if process.returncode == 0:
            self.message_signal.emit(
                f"Success: File {self.local_path} has been successfully uploaded to {self.remote_path}.", self.filename)
        else:
            error_message = process.stderr.read().strip()
            self.message_signal.emit(f"Failed:Failed to upload file {self.local_path}. Error: {error_message}",
                                     self.filename)
