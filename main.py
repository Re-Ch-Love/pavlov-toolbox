import os
import sys
from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from aria2.aria2 import Aria2
from features.common import ChineseMessageBox
from features.download_manager import DownloadManagerInterface
from features.browser_interface import ThemeSyncedWebViewInterface
import webbrowser
from qfluentwidgets import (
    FluentWindow,
    FluentIcon,
    InfoBar,
    InfoBarPosition,
    SplashScreen,
    Theme,
    setTheme,
)

from features.search import SearchInterface
from features.server_mod import ServerModInterface
from update_manager import CheckUpdateThread


# TODO: 将命名规则统一为驼峰
class AppMainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setMicaEffectEnabled(False)
        self.resize(900, 700)
        icon = QIcon(resource_abs_path("icon.ico"))
        app.setWindowIcon(icon)
        self.aria2 = Aria2()
        
        self.initInterfaces()
        self.startCheckUpdatesThread()

        # 创建启动页（用来掩盖首页WebEngineView的加载时间，不然显得加载很慢）
        self.splashScreen = SplashScreen(icon, self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()       
        # 2s后隐藏启动页
        QTimer.singleShot(2000, self.splashScreen.finish)

        
        self.aria2.startRpcServer()

    def initInterfaces(self):
        self.homeInterface = ThemeSyncedWebViewInterface(
            "home", "https://pavlov-toolbox.rech.asia/app-home", self
        )
        self.searchInterface = SearchInterface()
        self.serverModInterface = ServerModInterface()
        self.downloadManagerInterface = DownloadManagerInterface(self.aria2)
        self.helpInterface = ThemeSyncedWebViewInterface(
            "help", "https://pavlov-toolbox.rech.asia/usage", self
        )

        self.addSubInterface(self.homeInterface, FluentIcon.HOME, "首页")
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.searchInterface, FluentIcon.SEARCH, "搜索并安装Mod")
        self.addSubInterface(
            self.serverModInterface, FluentIcon.DICTIONARY_ADD, "安装服务器指定Mod"
        )
        self.addSubInterface(
            self.downloadManagerInterface, FluentIcon.CLOUD_DOWNLOAD, "管理Mod安装任务"
        )
        self.addSubInterface(
            ThemeSyncedWebViewInterface(
                "temp", "https://pavlov-toolbox.rech.asia/app-home", self
            ),
            FluentIcon.APPLICATION,
            "管理本地Mod",
        )  # TODO: 把本地Mod更新也放在这里面。Mod更新时对比API返回的taint和本地的taint，一次可以查询多个mod，使用参数id-in=2996823,2804502
        self.navigationInterface.addSeparator()
        self.addSubInterface(
            ThemeSyncedWebViewInterface(
                "temp2", "https://pavlov-toolbox.rech.asia/app-home", self
            ),
            FluentIcon.BOOK_SHELF,
            "游戏相关知识",
        )
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.helpInterface, FluentIcon.QUESTION, "帮助")
        # TODO: 加一个设置页，配置如下：
        # - 是否启用云母特效
        # - 是否自动下载依赖
        # - 是否自动安装

    def startCheckUpdatesThread(self):
        def onHasNewVersion(latest_version):
            msgBox = ChineseMessageBox(
                "发现新版本", f"最新版本：{latest_version}", self
            )
            msgBox.yesSignal.connect(
                lambda: webbrowser.open("https://pavlov-toolbox.rech.asia/download")
            )
            msgBox.yesButton.setText("前往下载")
            msgBox.exec()

        def onError(reason):
            InfoBar.error(
                title="检查更新失败",
                content=reason,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=5000,
                parent=self,
            )

        self.check_updates_thread = CheckUpdateThread()
        self.check_updates_thread.onHasNewVersion.connect(onHasNewVersion)
        self.check_updates_thread.onError.connect(onError)
        self.check_updates_thread.finished.connect(
            lambda: self.check_updates_thread.deleteLater()
        )
        self.check_updates_thread.start()


def resource_abs_path(relative_path):
    """将相对路径转为exe运行时资源文件的绝对路径"""
    if hasattr(sys, "_MEIPASS"):
        # 只有通过exe运行时才会进入这个分支，它返回的是exe运行时的临时目录路径
        base_path = sys._MEIPASS  # type: ignore
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    setTheme(Theme.LIGHT)
    app = QApplication()
    window = AppMainWindow()
    window.show()
    app.exec()
