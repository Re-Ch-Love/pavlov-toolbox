from functools import partial
from typing import List, Tuple
from PySide6.QtWidgets import QApplication, QSizePolicy, QWidget
from qfluentwidgets import InfoBar, InfoBarPosition, PrimaryPushButton

from common.common_ui import UneditableQTableWidgetItem
from common.mod.mod_data import ModData
from interfaces.local_mods_manager.presenter import LocalModsManagerPresenter
from ui_design.local_mods_manager_interface_ui import Ui_LocalModsManagerInterface


class LocalModsManagerView(QWidget, Ui_LocalModsManagerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.presenter = LocalModsManagerPresenter(self)
        self.presenter.loadMods()
        self.updateAllButton.clicked.connect(self.presenter.installAll)

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

    def loadModTable(self, data: List[Tuple[ModData, bool]]) -> None:
        """传入mod列表，和与之对应的是否是最新版的列表，根据此列表加载Mod数据"""
        self.modTable.setRowCount(len(data))
        for rowIndex, (mod, isLatest) in enumerate(data):
            # 设置第一列为更新按钮
            updateButton = PrimaryPushButton()
            updateButton.setText("更新")
            updateButton.setFixedSize(80, 30)
            updateButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            if isLatest:
                updateButton.setEnabled(False)
                # updateButton.setText("已是最新版")
                updateButton.setToolTip("已是最新版")
            else:
                updateButton.clicked.connect(partial(self.presenter.install, mod))
            self.modTable.setCellWidget(rowIndex, 0, updateButton)
            # 设置第二列为Mod资源ID
            self.modTable.setItem(rowIndex, 1, UneditableQTableWidgetItem(str(mod.resourceId)))
            # 设置第三列为Mod名称
            self.modTable.setItem(rowIndex, 2, UneditableQTableWidgetItem(mod.name))


def test1():
    app = QApplication()
    window = LocalModsManagerView()

    # window.presenter.loadMods()
    window.show()
    app.exec()


if __name__ == "__main__":
    test1()
