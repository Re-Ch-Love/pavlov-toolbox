from enum import Enum
from functools import partial
import json
from re import S
from PySide6 import QtNetwork
from PySide6.QtGui import QKeySequence
from qfluentwidgets import (
    InfoBar,
    InfoBarPosition,
    PrimaryPushButton,
    PushButton,
    RadioButton,
)
import urllib.parse
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QSizePolicy,
    QWidget,
)
from PySide6.QtCore import QUrl
from aria2.aria2 import Aria2
from aria2.aria2_with_data import Aria2WithData
from features.common import Mod, TargetNotFound, UneditableTableWidgetItem
from features.download_card import CardName, DownloadCard
from ui.search_interface_ui import Ui_SearchInterface


SEARCH_LIMIT = 10


class SearchInterface(QWidget):
    class SearchMode(Enum):
        modName = 1
        rid = 2

    def __init__(self, aria2wd: Aria2WithData):
        super().__init__()
        self.aria2wd = aria2wd
        self.ui = Ui_SearchInterface()
        self.ui.setupUi(self)
        # 初始化搜索栏
        self.ui.searchLineEdit.searchSignal.connect(self.search)
        # 设置主键区回车为快捷键
        self.ui.searchLineEdit.searchButton.setShortcut(QKeySequence("Return"))
        # 初始化搜索方式的单选按钮
        self.radioButtonGroup = QButtonGroup(self)
        self.radioButtonGroup.addButton(self.ui.modNameButton)
        self.radioButtonGroup.addButton(self.ui.ridButton)
        self.ui.modNameButton.setChecked(True)
        self.toggleSearchMode(self.ui.modNameButton)
        self.radioButtonGroup.buttonToggled.connect(self.toggleSearchMode)
        # 初始化搜索结果表格
        header = self.ui.resultTableWidget.horizontalHeader()
        # header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
        # 初始化 naManager
        self.naManager = QtNetwork.QNetworkAccessManager()

    def toggleSearchMode(self, button: RadioButton):
        if button.objectName() == self.ui.modNameButton.objectName():
            self.searchMode = SearchInterface.SearchMode.modName
            self.ui.searchLineEdit.setPlaceholderText("请输入Mod名称")
        elif button.objectName() == self.ui.ridButton.objectName():
            self.searchMode = SearchInterface.SearchMode.rid
            self.ui.searchLineEdit.setPlaceholderText("请输入Mod资源ID")

    def search(self, input):
        if input.strip() == "":
            return
        if self.searchMode == SearchInterface.SearchMode.modName:
            url = f"https://api.pavlov-toolbox.rech.asia/modio/v1/games/@pavlov/mods?_limit={SEARCH_LIMIT}&_sort=-popular&_q={urllib.parse.quote(input)}"
        elif self.searchMode == SearchInterface.SearchMode.rid:
            url = f"https://api.pavlov-toolbox.rech.asia/modio/v1/games/@pavlov/mods?_limit=1&id={urllib.parse.quote(input)}"
        else:
            InfoBar.error("软件内部发生错误", "")
            return
        request = QtNetwork.QNetworkRequest(QUrl(url))
        self.searchReply = self.naManager.get(request)
        self.searchReply.finished.connect(self.onSearchFinished)
        self.searchReply.errorOccurred.connect(self.onSearchErrorOccured)

    def onSearchErrorOccured(self, error):
        InfoBar.error(
            title="无法获取搜索结果",
            content=error.name,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=5000,
            parent=self,
        )
        self.searchReply.deleteLater()

    def onSearchFinished(self):
        if self.searchReply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
            return
        data = [
            Mod(itemData)
            for itemData in json.loads(
                bytes(self.searchReply.readAll().data()).decode()
            )["data"]
        ]
        if len(data) == 0:
            InfoBar.info(
                title="搜索完毕",
                content="没有找到相关的Mod",
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3000,
                parent=self,
            )
            return
        self.ui.resultTableWidget.setRowCount(len(data))

        for index, mod in enumerate(data):
            try:
                downloadUrl = mod.getWindowsDownloadUrl()
            except TargetNotFound:
                downloadUrl = ""
            modName = mod.getName()
            if downloadUrl:
                installButton = PrimaryPushButton()
                installButton.setText("安装")
                installButton.setFixedSize(80, 30)
                installButton.setSizePolicy(
                    QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
                )
                # 这里必须要用偏函数，不能用lambda闭包，否则下次循环时，downloadButton会被修改，则所有按钮的回调函数的参数都是同一个url
                installButton.clicked.connect(
                    partial(self.onInstall, installButton, downloadUrl, modName)
                )
                self.ui.resultTableWidget.setCellWidget(index, 0, installButton)
            else:
                self.ui.resultTableWidget.setItem(index, 0, UneditableTableWidgetItem("不可安装"))

            self.ui.resultTableWidget.setItem(
                index, 1, UneditableTableWidgetItem(str(mod.getResourceId()))
            )
            self.ui.resultTableWidget.setItem(
                index, 2, UneditableTableWidgetItem(modName)
            )

        self.searchReply.deleteLater()

    def onInstall(self, btnSelf: PushButton, url: str, displayName: str):
        btnSelf.setText("安装中")
        # TODO 需要创建一个Mod依赖管理器，添加下载链接时，发送给依赖管理器，依赖管理器检查依赖，然后再发送给下载管理器界面，这样可以显示displayName和hintName，例如依赖
        hintName = ""  # 等依赖管理器做好之后，hintName用来显示“XXX的依赖”这段文字，如果没有保留空字符串即可
        self.aria2wd.addUriWithData([url], CardName(displayName, hintName))


if __name__ == "__main__":
    app = QApplication()
    window = SearchInterface(Aria2WithData())
    window.show()
    app.exec()
