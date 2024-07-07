from PySide6.QtCore import QThread, Signal
import requests

from app_config import VERSION, Version


class UpdatesCheckThread(QThread):
    # 发送reason
    onError = Signal(str)
    onHasNewVersion = Signal(Version)

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        try:
            res = requests.get("https://api.pavlov-toolbox.rech.asia/latest-version")
        except requests.exceptions.ConnectionError:
            self.onError.emit(f"无法连接到服务器")
            return
        if res.status_code != 200:
            self.onError.emit("服务器发生错误")
            return
        latestVersionStr = res.content.decode().strip('"')
        x, y, z = latestVersionStr.split(".", 3)
        if not (x.isdigit() and y.isdigit() and z.isdigit()):
            self.onError.emit("服务器发生错误")
            return
        latestVersion = Version(int(x), int(y), int(z))
        x, y, z = int(x), int(y), int(z)
        if latestVersion > VERSION:
            self.onHasNewVersion.emit(latestVersion)


# TODO: 自动下载最新版
def downloadLatest():
    pass
