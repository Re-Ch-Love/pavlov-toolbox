from functools import partial
from typing import List, Tuple
from PySide6.QtWidgets import QApplication, QPushButton, QSizePolicy, QWidget
from qfluentwidgets import InfoBar, InfoBarPosition, PrimaryPushButton

from common.common_ui import UneditableQTableWidgetItem
from common.log import AppLogger, logThis
from common.mod.local_mods import ModStatusInLocal
from common.mod.mod_data import ModData
from ui.interfaces.i_refreshable import IRefreshable
from ui.local_mods_manager.presenter import LocalModsManagerPresenter
from ui_design.local_mods_manager_interface_ui import Ui_LocalModsManagerInterface


class LocalModsManagerView(QWidget, Ui_LocalModsManagerInterface, IRefreshable):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.presenter = LocalModsManagerPresenter(self)
        self.updateAllButton.clicked.connect(self.presenter.installAll)
        # API响应比较慢，所以需要预加载，这个方法是异步的，不用担心会阻塞
        self.presenter.loadMods()

    def refresh(self):
        self.presenter.loadMods()

    def onInstall(self, button: QPushButton, modData: ModData):
        button.setText("安装中")
        button.setEnabled(False)
        InfoBar.info(
            title="已添加安装任务",
            content="请前往“管理Mod安装任务”查看",
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=3000,
            parent=self,
        )
        self.presenter.install(modData)

    def showInstallMsg(self):
        InfoBar.info(
            title="已添加安装任务",
            content="请前往“管理Mod安装任务”查看",
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=3000,
            parent=self,
        )

    def disableAllButton(self):
        for rowIndex in range(self.modTable.rowCount()):
            button = self.modTable.cellWidget(rowIndex, 0)
            button.setEnabled(False)

    def loadModTable(
        self, modDataList: List[ModData], modStatusInLocalList: List[ModStatusInLocal]
    ) -> None:
        """传入mod列表，和与之对应的是否是最新版的列表，根据此列表加载Mod数据"""
        self.modTable.setRowCount(len(modDataList))
        for rowIndex, (modData, modStatusInLocal) in enumerate(
            zip(modDataList, modStatusInLocalList)
        ):
            # 设置第一列为更新按钮
            updateButton = PrimaryPushButton()
            updateButton.setText("更新")
            updateButton.setFixedSize(80, 30)
            updateButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            updateButton.clicked.connect(partial(self.onInstall, updateButton, modData))
            match modStatusInLocal:
                case ModStatusInLocal.INSTALLED_AND_LATEST:
                    updateButton.setText("已是最新")
                    updateButton.setEnabled(False)
                case ModStatusInLocal.OUTDATED:
                    updateButton.setText("更新")
                case ModStatusInLocal.INSTALLING:
                    updateButton.setText("安装中")
                    updateButton.setEnabled(False)
                case ModStatusInLocal.NOT_INSTALLED:
                    AppLogger().warning("为本地Mod传入的Mod状态为未安装")
                case _:
                    AppLogger().warning("传入的Mod状态不合法")
                    updateButton.setText("未知状态")
                    updateButton.setEnabled(False)
            self.modTable.setCellWidget(rowIndex, 0, updateButton)
            # 设置第二列为Mod资源ID
            self.modTable.setItem(rowIndex, 1, UneditableQTableWidgetItem(str(modData.resourceId)))
            # 设置第三列为Mod名称
            self.modTable.setItem(rowIndex, 2, UneditableQTableWidgetItem(modData.name))


def test1():
    app = QApplication()
    window = LocalModsManagerView()
    window.show()
    app.exec()


if __name__ == "__main__":
    test1()
