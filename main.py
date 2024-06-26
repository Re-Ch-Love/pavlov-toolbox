import os
import sys
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QThread, Slot, Signal
from PySide6.QtGui import QIcon
import requests
from features.search import SearchWidget
from features.unzip_and_complete import UnzipAndCompleteWidget
from ui.common import exec_simple_dialog
from ui.main_ui import Ui_MainWindow
from features.get_dl_url import GetDlUrlWidget
import webbrowser

VERSION = {"x": 0, "y": 2, "z": 0}


def checkUpdates(silence: bool):
    try:
        res = requests.get("https://pavlov.rech.asia/latest-version")
    except requests.exceptions.ConnectionError as e:
        exec_simple_dialog("错误", f"无法连接到更新检查服务器。\n详细信息：{e}")
        return
    if res.status_code != 200:
        exec_simple_dialog("错误", "更新检查服务器发生错误，请稍后再试。")
        return
    target_version = res.content.decode().strip('"')
    x, y, z = target_version.split(".", 3)
    if not (x.isdigit() and y.isdigit() and z.isdigit()):
        exec_simple_dialog("错误", "更新检查服务器发生错误，请稍后再试。")
        return
    x, y, z = int(x), int(y), int(z)
    # 只要每个数字都不大于1000，该算法就可以工作
    target_version_sum = x * 1000_000 + y * 1000 + z
    current_version_sum = VERSION["x"] * 1000_000 + VERSION["y"] * 1000 + VERSION["z"]
    current_version = ".".join(
        [str(n) for n in [VERSION["x"], VERSION["y"], VERSION["z"]]]
    )
    # print(target_version_sum, current_version_sum)
    if target_version_sum > current_version_sum:
        exec_simple_dialog(
            "检查完毕",
            f"当前版本：{current_version}\n最新版：{target_version}",
            pbtnText="点击按钮下载最新版",
            onPbtnClick=lambda: webbrowser.open(
                "https://pavlovtoolbox.rech.asia/download"
            ),
        )
    elif not silence:
        exec_simple_dialog(
            "检查完毕", f"您所使用的版本{current_version}已经是最新版了。"
        )


class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.act_getModDlUrl.triggered.connect(
            lambda: self.setCentralWidget(GetDlUrlWidget())
        )
        self.ui.act_unzipAndCompletion.triggered.connect(
            lambda: self.setCentralWidget(UnzipAndCompleteWidget())
        )
        self.ui.act_search.triggered.connect(
            lambda: self.setCentralWidget(SearchWidget())
        )
        self.ui.act_usage.triggered.connect(
            lambda: webbrowser.open("https://pavlovtoolbox.rech.asia/usage")
        )
        self.ui.act_notice.triggered.connect(
            lambda: webbrowser.open("https://pavlovtoolbox.rech.asia/notice")
        )
        self.ui.act_checkUpdates.triggered.connect(lambda: checkUpdates(False))

    def startCheckUpdatesThread(self):
        @Slot(str)
        def onHasNewVersion(target_version):
            exec_simple_dialog(
                "发现新版本",
                f"发现新版本：{target_version}",
                pbtnText="点击按钮下载最新版",
                onPbtnClick=lambda: webbrowser.open(
                    "https://pavlovtoolbox.rech.asia/download"
                ),
            )

        @Slot(str)
        def onError(reason):
            window.ui.statusbar.showMessage(f"检查更新失败：{reason}", 6000)

        self.check_updates_thread = CheckUpdates()
        self.check_updates_thread.onHasNewVersion.connect(onHasNewVersion)
        self.check_updates_thread.onError.connect(onError)
        self.check_updates_thread.finished.connect(lambda: self.check_updates_thread.deleteLater())
        self.check_updates_thread.start()


class CheckUpdates(QThread):
    onError = Signal(str)
    # 发送一个版本号
    onHasNewVersion = Signal(str)

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        try:
            res = requests.get("https://pavlov.rech.asia/latest-version")
        except requests.exceptions.ConnectionError as e:
            self.onError.emit(f"无法连接到更新检查服务器。\n详细信息：{e}")
            return
        if res.status_code != 200:
            self.onError.emit("更新检查服务器发生错误，请稍后再试。")
            return
        target_version = res.content.decode().strip('"')
        x, y, z = target_version.split(".", 3)
        if not (x.isdigit() and y.isdigit() and z.isdigit()):
            self.onError.emit("更新检查服务器发生错误，请稍后再试。")
            return
        x, y, z = int(x), int(y), int(z)
        # 只要每个数字都不大于1000，该算法就可以工作
        target_version_sum = x * 1000_000 + y * 1000 + z
        current_version_sum = (
            VERSION["x"] * 1000_000 + VERSION["y"] * 1000 + VERSION["z"]
        )
        # current_version = ".".join(
        #     [str(n) for n in [version["x"], version["y"], version["z"]]]
        # )
        # print(target_version_sum, current_version_sum)
        if target_version_sum > current_version_sum:
            self.onHasNewVersion.emit(target_version)

def resource_abs_path(relative_path):
    """将相对路径转为exe运行时资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        # 只有通过exe运行时才会进入这个分支，它返回的是exe运行时的临时目录路径
        base_path = sys._MEIPASS		# type: ignore
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    app = QApplication()
    icon = QIcon(resource_abs_path("icon.png"))
    app.setWindowIcon(icon)
    window = AppMainWindow()
    window.show()
    window.startCheckUpdatesThread()
    app.exec()
