import webbrowser

from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import (
    FluentWindow,
    FluentIcon,
    InfoBar,
    InfoBarPosition,
    SplashScreen,
    Theme,
    setTheme,
)

from app_config import VERSION, Version
from common.common_ui import ChineseMessageBox
from common.mod.installation.mod_download_manager import ModDownloadManager
from common.path import getResourcePath
from common.qrequest import QRequestReady
from common.log import AppLogger, initAppLogEnvironment
from ui.interfaces.i_freezable import IFreezable
from ui.interfaces.i_refreshable import IRefreshable
from ui.installation.view import ModInstallationManagerView
from ui.local_mods_manager.view import LocalModsManagerView
from ui.search.view import SearchView
from ui.server_mod.view import ServerModView
from ui.settings.view import SettingsView
from ui.webview.webview_interface import PavlovToolboxWebsiteInterface


class AppMainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        # 设置主题为亮色
        setTheme(Theme.LIGHT)
        # 禁用云母特效，否则和WebView搭配太丑了（WebView底色不透明）
        self.setMicaEffectEnabled(False)
        self.resize(1000, 700)
        # 设置icon
        icon = QIcon(getResourcePath("icon.ico"))
        app.setWindowIcon(icon)

        # 默认展开边栏
        self.navigationInterface.setExpandWidth(200)
        self.navigationInterface.setCollapsible(False)

        self.stackedWidget.currentChanged.connect(self.onInterfaceChanged)

        self.initInterfaces()

        # 创建启动页（用来掩盖首页WebEngineView的加载时间，不然显得加载很慢）
        self.splashScreen = SplashScreen(icon, self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()

        # 检查更新
        self.checkUpdates()

        # 2s后隐藏启动页
        QTimer.singleShot(2000, self.splashScreen.finish)

    def initInterfaces(self):
        self.homeInterface = PavlovToolboxWebsiteInterface(
            "https://pavlov-toolbox.rech.asia/app-home",
            self,
            isRemoveToolButtons=True,
            disableATagsJump=True,
        )
        self.searchInterface = SearchView()
        self.serverModInterface = ServerModView()
        self.downloadManagerInterface = ModInstallationManagerView()
        self.localModsManagerInterface = LocalModsManagerView()
        self.knowledgeBaseInterface = PavlovToolboxWebsiteInterface(
            "https://pavlov-toolbox.rech.asia/knowledge-base", self
        )
        self.aboutInterface = PavlovToolboxWebsiteInterface(
            "https://pavlov-toolbox.rech.asia/about", self
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
        """
        currentInterface = self.stackedWidget.currentWidget()
        # 遍历所有的interface
        for index in range(self.stackedWidget.count()):
            interface = self.stackedWidget.widget(index)
            # 如果该界面是当前界面，则调用其refresh方法刷新界面
            if interface is currentInterface:
                if isinstance(currentInterface, IRefreshable):
                    currentInterface.refresh()
            # 如果该界面不是当前界面，则调用其freeze方法冻结界面（例如停止轮询）
            else:
                if isinstance(interface, IFreezable):
                    interface.freeze()

    def checkUpdates(self):
        # 判断是否需要更新
        def decideIsNeedUpdate(res: bytes) -> None | bool:
            latestVersionStr = res.decode().strip('"')
            x, y, z = latestVersionStr.split(".", 3)
            if not (x.isdigit() and y.isdigit() and z.isdigit()):
                # 如果服务器返回的格式有问题，则认为不需要更新
                return False
            latestVersion = Version(int(x), int(y), int(z))
            x, y, z = int(x), int(y), int(z)
            return latestVersion > VERSION

        def updateIfNeed(needUpdate: bool):
            if not needUpdate:
                return
            msgBox = ChineseMessageBox("发现新版本", f"请点击按钮升级", self)
            # 隐藏取消按钮
            msgBox.cancelButton.hide()
            msgBox.buttonLayout.insertStretch(1)
            msgBox.yesSignal.connect(
                lambda: webbrowser.open("https://api.pavlov-toolbox.rech.asia/download/latest")
            )
            msgBox.yesButton.setText("前往下载")
            msgBox.exec()

        def onRequestError():
            InfoBar.error(
                title="检查更新失败",
                content="请检查网络连接（无网络时无法使用该工具箱）",
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3000,
                parent=self,
            )

        (
            QRequestReady(app)
            .get("https://api.pavlov-toolbox.rech.asia/latest-version")
            .then(decideIsNeedUpdate)
            .then(updateIfNeed)
            .catch(onRequestError)
            .done()
        )

    def closeEvent(self, e):
        aria2 = ModDownloadManager.getInstance().aria2c
        # 终止aria2进程
        aria2.process.terminate()
        # 等待aria2的进程结束（否则打包后清理临时资源时会出错（应该是因为aria2c.exe占用））
        aria2.process.wait(timeout=3)  # 设置3秒超时
        # 如果进程还在运行，则kill
        if aria2.process.poll() is None:
            aria2.process.kill()
        e.accept()
        AppLogger().info(f"App关闭")


if __name__ == "__main__":
    initAppLogEnvironment()
    AppLogger().info(f"App启动")
    app = QApplication()
    window = AppMainWindow()
    window.show()
    app.exec()
