import os
import sys
import PySide6
from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
import webbrowser
from qfluentwidgets import (
    FluentWindow,
    FluentIcon,
    InfoBar,
    InfoBarPosition,
    Signal,
    SplashScreen,
    Theme,
    setTheme,
)
from features.common.ui import ChineseMessageBox
from features.installation.view import DownloadManagerView
from features.search.view import SearchView
from features.server_mod.server_mod import ServerModInterface
from features.settings.view import SettingsView
from features.webview.webview_interface import PavlovToolboxWebsiteInterface
from update_manager import UpdatesCheckThread


class AppMainWindow(FluentWindow):
    # spell-checker: disable-next-line
    # 用于在多个webview间同步主题，因为没有找到相关文档，为了避免bug，所以不用qconfig.themeChangedFinished 
    # 发射对应WebViewInterface的uniqueName，防止自己发射自己接收，导致多运行一次
    themeToggleSyncSignal = Signal(str)
    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug
        # 设置云母特效
        # self.setMicaEffectEnabled(False)
        self.resize(1000, 700)
        icon = QIcon(resourceAbsPath("icon.ico"))
        app.setWindowIcon(icon)

        self.initInterfaces()
        self.startCheckUpdatesThread()
        self.navigationInterface.setExpandWidth(200)
        self.navigationInterface.setCollapsible(False)

        self.stackedWidget.currentChanged.connect(self.onInterfaceChanged)

        # 创建启动页（用来掩盖首页WebEngineView的加载时间，不然显得加载很慢）
        self.splashScreen = SplashScreen(icon, self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()
        # 2s后隐藏启动页
        QTimer.singleShot(2000, self.splashScreen.finish)

    def initInterfaces(self):
        self.homeInterface = PavlovToolboxWebsiteInterface(
            "home", "https://pavlov-toolbox.rech.asia/app-home", self
        )
        self.searchInterface = SearchView()
        self.serverModInterface = ServerModInterface()
        self.downloadManagerInterface = DownloadManagerView()
        self.helpInterface = PavlovToolboxWebsiteInterface(
            "help", "https://pavlov-toolbox.rech.asia/usage", self
        )
        self.settingsInterface = SettingsView()

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
            PavlovToolboxWebsiteInterface(
                "temp", "https://pavlov-toolbox.rech.asia/app-home", self
            ),
            FluentIcon.APPLICATION,
            "管理本地Mod",
        )  # TODO: 把本地Mod更新也放在这里面。Mod更新时对比API返回的taint和本地的taint，一次可以查询多个mod，使用参数id-in=2996823,2804502
        self.navigationInterface.addSeparator()
        self.addSubInterface(
            PavlovToolboxWebsiteInterface(
                "temp2", "https://pavlov-toolbox.rech.asia/app-home", self
            ),
            FluentIcon.BOOK_SHELF,
            "游戏相关知识",
        )
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.helpInterface, FluentIcon.QUESTION, "帮助")
        self.addSubInterface(self.settingsInterface, FluentIcon.SETTING, "设置")

    def onInterfaceChanged(self):
        """
        当界面切换时触发

        当切换到下载界面时，通知其轮询下载进度等信息。
        当不是下载界面时，停止这些操作以节约资源。
        """
        self.downloadManagerInterface.showStatusChanged.emit(
            self.stackedWidget.currentWidget() is self.downloadManagerInterface
        )

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

        self.updateCheckThread = UpdatesCheckThread()
        self.updateCheckThread.onHasNewVersion.connect(onHasNewVersion)
        self.updateCheckThread.onError.connect(onError)
        self.updateCheckThread.finished.connect(
            lambda: self.updateCheckThread.deleteLater()
        )
        self.updateCheckThread.start()


def resourceAbsPath(relativePath):
    """将相对路径转为exe运行时资源文件的绝对路径"""
    if hasattr(sys, "_MEIPASS"):
        # 只有通过exe运行时才会进入这个分支，它返回的是exe运行时的临时目录路径
        basePath = sys._MEIPASS  # type: ignore
    else:
        basePath = os.path.abspath(".")
    return os.path.join(basePath, relativePath)


if __name__ == "__main__":
    # setTheme(Theme.LIGHT)
    app = QApplication()
    window = AppMainWindow(debug=True)
    window.show()
    app.exec()
