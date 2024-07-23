from functools import partial
from typing import List, cast
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QPushButton, QSizePolicy, QWidget
from PySide6 import QtNetwork

from qfluentwidgets import InfoBar, InfoBarPosition, PrimaryPushButton

from common.common_ui import UneditableQTableWidgetItem
from common.log import AppLogger
from common.mod.local_mods import ModStatusInLocal
from common.mod.mod_data import ModData
from ui.interfaces.i_refreshable import IRefreshable
from ui.server_mod.presenter import ServerModPresenter
from ui_design.server_interface_ui import Ui_ServerModInterface


class ServerModView(QWidget, Ui_ServerModInterface, IRefreshable):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.naManager = QtNetwork.QNetworkAccessManager()
        self.presenter = ServerModPresenter(self)
        self.presenter.loadServersModList()
        self.serverComboBox.setPlaceholderText("请选择一个服务器")
        self.serverComboBox.currentIndexChanged.connect(self.presenter.loadModTable)
        self.installAllButton.clicked.connect(self.presenter.installAllMod)

    def refresh(self) -> None:
        self.presenter.loadModTable(self.serverComboBox.currentIndex())

    def showAddJobInfo(self):
        InfoBar.info(
            title="已添加安装任务",
            content="请前往“管理Mod安装任务”查看",
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=1500,
            parent=self,
        )

    def disableAllButtonInTable(self):
        for rowIndex in range(self.tableWidget.rowCount()):
            button = cast(QPushButton, self.tableWidget.cellWidget(rowIndex, 0))
            if button.isEnabled():
                button.setText("安装中")
                button.setEnabled(False)

    def showMods(self, modDataList: List[ModData], modStatusInLocalList: List[ModStatusInLocal]):
        self.tableWidget.setRowCount(len(modDataList))

        for index, (modData, modStatusInLocal) in enumerate(zip(modDataList, modStatusInLocalList)):
            # 设置状态item
            installButton = PrimaryPushButton()
            installButton.setFixedSize(80, 30)
            installButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            installButton.clicked.connect(
                partial(self.presenter.installMod, installButton, modData)
            )
            match modStatusInLocal:
                case ModStatusInLocal.INSTALLED_AND_LATEST:
                    installButton.setText("已安装")
                    installButton.setEnabled(False)
                case ModStatusInLocal.NOT_INSTALLED:
                    installButton.setText("安装")
                case ModStatusInLocal.OUTDATED:
                    installButton.setText("更新")
                case ModStatusInLocal.INSTALLING:
                    installButton.setText("安装中")
                    installButton.setEnabled(False)
                case _:
                    AppLogger().warning("传入的Mod状态不合法")
                    installButton.setText("未知状态")
                    installButton.setEnabled(False)
            self.tableWidget.setCellWidget(index, 0, installButton)
            # 设置资源ID item
            ridItem = UneditableQTableWidgetItem(str(modData.resourceId))
            ridItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.tableWidget.setItem(index, 1, ridItem)
            # 设置名称item
            nameItem = UneditableQTableWidgetItem(modData.name)
            nameItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.tableWidget.setItem(index, 2, nameItem)

    def showServersModList(self, names: List[str]):
        self.serverComboBox.addItems(names)
        # self.serverComboBox.setCurrentIndex(-1)

    def showNetworkErrorInfo(self, reason):
        InfoBar.error(
            title="网络请求失败",
            content=reason,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=3000,
            parent=self,
        )


if __name__ == "__main__":
    app = QApplication()
    window = ServerModView()
    window.show()
    app.exec()
