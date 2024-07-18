from functools import partial
import json
from typing import Any, Dict, List, Optional
from PySide6 import QtCore
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QTableWidgetItem, QWidget
from PySide6 import QtNetwork

from qfluentwidgets import InfoBar, InfoBarPosition

from common.common_ui import UneditableQTableWidgetItem
from common.mod.local_mods import getLocalMods
from common.mod.mod_data import MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST, ModData, modBatchRequest
from common.mod.mod_installation import ModInstallationManager
from common.qrequest import QRequestReady
from ui_design.server_interface_ui import Ui_ServerModInterface

SERVERS_MOD_LIST_URL = "https://api.pavlov-toolbox.rech.asia/servers-mod-list"


class ServerModInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ServerModInterface()
        self.ui.setupUi(self)
        self.naManager = QtNetwork.QNetworkAccessManager()
        self.serversModList: Optional[List[Dict[str, Any]]] = None
        self.initServerComboBox()
        self.ui.serverComboBox.currentIndexChanged.connect(self.updateTableWidget)
        self.ui.installButton.clicked.connect(self.onInstallButtonClicked)
        self.selectedMods: List[ModData] = []

    def onInstallButtonClicked(self):
        if not self.selectedMods:
            return
        InfoBar.info(
            title="已添加安装任务",
            content="请前往“管理Mod安装任务”查看",
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=3000,
            parent=self,
        )
        for mod in self.selectedMods:
            ModInstallationManager.getInstance().addJob(mod)

    def updateTableWidget(self, serverIndex: int):
        if self.serversModList is None or serverIndex < 0:
            return
        ridList: List[int] = self.serversModList[serverIndex]["ridList"]
        self.ui.tableWidget.setRowCount(len(ridList))
        for index, rid in enumerate(ridList):
            item = UneditableQTableWidgetItem(str(rid))
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(index, 1, item)
        self.modBatchReplies: List[QtNetwork.QNetworkReply] = modBatchRequest(
            self.naManager,
            ridList,
            partial(self.onTableModNameFinished, serverIndex),
            self.onTableModNameErrorOccurred,
        )

    def onTableModNameFinished(self, currentServerModListIndex: int, replyIndex: int):
        if (
            self.serversModList is None
            or self.modBatchReplies[replyIndex].error()
            != QtNetwork.QNetworkReply.NetworkError.NoError
        ):
            return

        result = json.loads(bytes(self.modBatchReplies[replyIndex].readAll().data()).decode())
        resultModList = [ModData(item) for item in result["data"]]
        self.selectedMods = resultModList
        # 返回值的顺序与界面中rid的顺序不一定是一致的，因此需要进行排序
        ridModMap: Dict[int, ModData] = {}
        for mod in resultModList:
            ridModMap[mod.resourceId] = mod
        serverRidList = self.serversModList[currentServerModListIndex]["ridList"]
        sortedModList = [ridModMap[rid] for rid in serverRidList if rid in ridModMap]
        localMods = getLocalMods()
        localModRids = [localMod.resourceId for localMod in localMods]
        # 填充数据
        for index, mod in enumerate(sortedModList):
            index += MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST * replyIndex
            # 设置名称item
            item = UneditableQTableWidgetItem(mod.name)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(index, 2, item)
            # 设置状态item
            # 如果当前mod在localMods的rid中，且localMod的taint与mod的file live windows一致，则显示为已安装
            # 如果在rid中，但taint不一致，则显示为需更新
            # 如果不在rid中，显示为未安装
            item: QTableWidgetItem
            if mod.resourceId in localModRids:
                matchedLocalMod = next(
                    (localMod for localMod in localMods if localMod.resourceId == mod.resourceId)
                )
                if matchedLocalMod.taint == mod.getModFileLive("windows"):
                    item = UneditableQTableWidgetItem("✔已安装")
                else:
                    item = UneditableQTableWidgetItem("✘需更新")
            else:
                item = UneditableQTableWidgetItem("✘未安装")
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(index, 0, item)
        self.modBatchReplies[replyIndex].deleteLater()

    def onTableModNameErrorOccurred(
        self, replyIndex: int, error: QtNetwork.QNetworkReply.NetworkError
    ):
        InfoBar.error(
            title="无法获取搜索结果",
            content=error.name,
            position=InfoBarPosition.BOTTOM_RIGHT,
            parent=self,
        )
        self.modBatchReplies[replyIndex].deleteLater()

    def initServerComboBox(self):
        self.ui.serverComboBox.setPlaceholderText("请选择一个服务器")
        request = QtNetwork.QNetworkRequest(QUrl(SERVERS_MOD_LIST_URL))
        self.serversModListReply = self.naManager.get(request)
        self.serversModListReply.finished.connect(self.onGetServersModListFinished)
        self.serversModListReply.errorOccurred.connect(self.onGetServersModListErrorOccurred)

    def onGetServersModListFinished(self):
        if self.serversModListReply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
            return
        data = bytes(self.serversModListReply.readAll().data()).decode()
        obj = json.loads(data)
        self.serversModList = obj
        self.ui.serverComboBox.addItems([o["serverName"] for o in obj])
        # self.ui.serverComboBox.setCurrentIndex(-1)

    def onGetServersModListErrorOccurred(self):
        InfoBar.error(
            title="网络请求失败",
            content=self.serversModListReply.error().name,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=5000,
            parent=self,
        )


if __name__ == "__main__":
    app = QApplication()
    window = ServerModInterface()
    window.show()
    # app.exec()
