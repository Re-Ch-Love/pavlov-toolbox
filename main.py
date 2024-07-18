import os
import sys
import webbrowser

from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import (
    FluentWindow,
    FluentIcon,
    InfoBar,
    InfoBarPosition,
    Signal,
    SplashScreen,
)

from common.common_ui import ChineseMessageBox
from interfaces.installation.view import ModInstallationManagerView
from interfaces.local_mods_manager.view import LocalModsManagerView
from interfaces.search.view import SearchView
from interfaces.server_mod.server_mod import ServerModInterface
from interfaces.settings.view import SettingsView
from interfaces.webview.webview_interface import PavlovToolboxWebsiteInterface


class AppMainWindow(FluentWindow):
    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug
        # 禁用云母特效，否则和WebView搭配太丑了（WebView底色不透明）
        self.setMicaEffectEnabled(False)
        self.resize(1000, 700)
        icon = QIcon(resourceAbsPath("icon.ico"))
        app.setWindowIcon(icon)

        self.initInterfaces()

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
            "home",
            "https://pavlov-toolbox.rech.asia/app-home",
            self,
            isRemoveToolButtons=True,
            disableATagsJump=True,
        )
        self.searchInterface = SearchView()
        self.serverModInterface = ServerModInterface()
        self.downloadManagerInterface = ModInstallationManagerView()
        self.localModsManagerInterface = LocalModsManagerView()
        self.knowledgeBaseInterface = PavlovToolboxWebsiteInterface(
            "knowledge_base", "https://pavlov-toolbox.rech.asia/knowledge-base", self
        )
        self.aboutInterface = PavlovToolboxWebsiteInterface(
            "about", "https://pavlov-toolbox.rech.asia/about", self
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
            self.localModsManagerInterface,
            FluentIcon.APPLICATION,
            "管理本地Mod",
        )
        self.navigationInterface.addSeparator()
        self.addSubInterface(
            self.knowledgeBaseInterface,
            FluentIcon.BOOK_SHELF,
            "游戏知识库",
        )
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.aboutInterface, FluentIcon.INFO, "关于")
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


def resourceAbsPath(relativePath: str) -> str:
    """将相对路径转为exe运行时资源文件的绝对路径"""

    if hasattr(sys, "_MEIPASS"):
        # 只有通过exe运行时才会进入这个分支，它返回的是exe运行时的临时目录路径
        # noinspection PyProtectedMember
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
