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
)

from app_config import VERSION, Version
from common.common_ui import ChineseMessageBox
from common.path import getResourcePath
from common.qrequest import QRequestReady
from interfaces.installation.view import ModInstallationManagerView
from interfaces.local_mods_manager.view import LocalModsManagerView
from interfaces.search.view import SearchView
from interfaces.server_mod.server_mod import ServerModInterface
from interfaces.settings.view import SettingsView
from interfaces.webview.webview_interface import PavlovToolboxWebsiteInterface


class AppMainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        # 禁用云母特效，否则和WebView搭配太丑了（WebView底色不透明）
        self.setMicaEffectEnabled(False)
        self.resize(1000, 700)
        icon = QIcon(getResourcePath("icon.ico"))
        app.setWindowIcon(icon)

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

    def checkUpdates(self):
        # 判断是否需要更新
        def judgeIsNeedUpdate(res: bytes) -> None | bool:
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
            .then(judgeIsNeedUpdate)
            .then(updateIfNeed)
            .catch(onRequestError)
            .done()
        )

    def closeEvent(self, e):
        from common.mod.mod_installation import aria2

        # 终止aria2进程
        aria2.process.terminate()
        # 等待aria2的进程结束（否则打包后清理临时资源时会出错（应该是因为aria2c.exe占用））
        aria2.process.wait(timeout=3)  # 设置3秒超时
        # 如果进程还在运行，则kill
        if aria2.process.poll() is None:
            aria2.process.kill()
        e.accept()

        # 下面这段代码是用aria2.shutdown()来关闭，然后等待，但这样太慢了
        # 似乎aria2.forceShutdown()也很慢

        # isAccepted = False

        # def acceptEvent():
        #     nonlocal isAccepted
        #     if isAccepted:
        #         return
        #     isAccepted = True
        #     # 向aria2发送shutdown信号
        #     # aria2.shutdown()
        #     aria2.process.terminate()
        #     # 然后等待它的进程结束（否则打包后清理临时资源时会出错）
        #     aria2.process.wait(timeout=5)  # 设置5秒超时
        #     e.accept()

        # def ignoreEvent():
        #     e.ignore()

        # msgBox = ChineseMessageBox(
        #     "确定要关闭 Pavlov 工具箱吗？",
        #     "为确保下载引擎被正确关闭，点击“确定”后软件会短暂卡顿，请耐心等待！",
        #     self,
        # )
        # msgBox.yesButton.clicked.connect(acceptEvent)
        # msgBox.cancelButton.clicked.connect(ignoreEvent)
        # msgBox.exec()


if __name__ == "__main__":
    # setTheme(Theme.LIGHT)
    app = QApplication()
    window = AppMainWindow()
    window.show()
    app.exec()
