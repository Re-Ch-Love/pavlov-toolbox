from enum import Enum
import json
from PySide6 import QtNetwork
from PySide6.QtGui import QKeySequence
from qfluentwidgets import InfoBar, InfoBarPosition, PrimaryPushButton, RadioButton
import urllib.parse
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QSizePolicy,
    QWidget,
)
from PySide6.QtCore import QUrl
from ui.search_interface_ui import Ui_SearchInterface
from features.common import *


SEARCH_LIMIT = 10


class SearchInterface(QWidget):
    class SearchMode(Enum):
        modName = 1
        rid = 2

    def __init__(self):
        super().__init__()
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
            # try:
            #     downloadUrl = mod.getWindowsDownloadUrl()
            # except TargetNotFound:
            #     downloadUrl = "无法获取"
            downloadButton = PrimaryPushButton()
            downloadButton.setText("安装")
            downloadButton.setFixedSize(80, 30)
            downloadButton.setSizePolicy(
                QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
            )
            self.ui.resultTableWidget.setCellWidget(index, 0, downloadButton)
            self.ui.resultTableWidget.setItem(
                index, 1, UneditableTableWidgetItem(str(mod.getResourceId()))
            )
            self.ui.resultTableWidget.setItem(
                index, 2, UneditableTableWidgetItem(mod.getName())
            )

        self.searchReply.deleteLater()


if __name__ == "__main__":
    app = QApplication()
    window = SearchInterface()
    window.show()
    app.exec()
