from abc import ABC, abstractmethod
from functools import partial
from typing import List
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence
from qfluentwidgets import (
    InfoBar,
    InfoBarPosition,
    PrimaryPushButton,
    PushButton,
    RadioButton,
)

from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QSizePolicy,
    QWidget,
)
from generated_ui.search_interface_ui import Ui_SearchInterface
from features.common.ui import UneditableQTableWidgetItem
from features.common.mod import ModData, ModInfoNotFound
from features.search.common import SearchMode
from features.search.presenter import SearchPresenter


class SearchView(QWidget, Ui_SearchInterface):

    def __init__(self):
        super().__init__()
        self.presenter = SearchPresenter(self)
        self.setupUi(self)
        # 初始化搜索栏
        self.searchLineEdit.searchSignal.connect(self.presenter.search)
        # 设置主键区回车为快捷键
        self.searchLineEdit.searchButton.setShortcut(QKeySequence("Return"))
        # 初始化搜索方式的单选按钮
        self.radioButtonGroup = QButtonGroup(self)
        self.radioButtonGroup.addButton(self.modNameButton)
        self.radioButtonGroup.addButton(self.ridButton)
        self.modNameButton.setChecked(True)
        self._toggleSearchMode(self.modNameButton)
        self.radioButtonGroup.buttonToggled.connect(self._toggleSearchMode)
        # 初始化搜索结果表格
        header = self.resultTableWidget.horizontalHeader()
        header.setStretchLastSection(True)

    def _toggleSearchMode(self, button: RadioButton):
        if button.objectName() == self.modNameButton.objectName():
            mode = SearchMode.modName
        elif button.objectName() == self.ridButton.objectName():
            mode = SearchMode.rid
        else:
            raise Exception("Unknown button name")
        self._setSearchHint(mode)
        self.presenter.setSearchMode(mode)

    def _setSearchHint(self, mode: SearchMode):
        match mode:
            case SearchMode.modName:
                self.searchLineEdit.setPlaceholderText("请输入Mod名称")
            case SearchMode.rid:
                self.searchLineEdit.setPlaceholderText("请输入Mod资源ID")

    def promptSearchError(self, reason: str):
        InfoBar.error(
            title="无法获取搜索结果",
            content=reason,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=5000,
            parent=self,
        )

    def promptNoSearchResult(self):
        InfoBar.info(
            title="搜索完毕",
            content="没有找到相关的Mod",
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=3000,
            parent=self,
        )

    def showResult(self, data: List[ModData]):
        self.resultTableWidget.setRowCount(len(data))

        for index, mod in enumerate(data):
            try:
                downloadUrl = mod.getWindowsDownloadUrl()
            except ModInfoNotFound:
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
                self.resultTableWidget.setCellWidget(index, 0, installButton)
            else:
                item = UneditableQTableWidgetItem("不可安装")
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
                )
                self.resultTableWidget.setItem(index, 0, item)

            self.resultTableWidget.setItem(
                index, 1, UneditableQTableWidgetItem(str(mod.getResourceId()))
            )
            self.resultTableWidget.setItem(
                index, 2, UneditableQTableWidgetItem(modName)
            )

    def onInstall(self, pbtn: PushButton, url: str, modName: str):
        pbtn.setText("安装中")
        self.presenter.install(url, modName)


if __name__ == "__main__":
    app = QApplication()
    window = SearchView()
    window.show()
    window.presenter.search("inferno")
    app.exec()
