from functools import partial
import json
from typing import Any, Dict, List, Optional
from PySide6 import QtCore
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QWidget
from PySide6 import QtNetwork
from features.common import MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST, Mod, UneditableTableWidgetItem, modBatchRequest
from ui.server_interface_ui import Ui_ServerModInterface
from qfluentwidgets import InfoBar, InfoBarPosition

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

    def updateTableWidget(self, serverIndex: int):
        if self.serversModList is None or serverIndex < 0:
            return
        ridList: List[int] = self.serversModList[serverIndex]["ridList"]
        self.ui.tableWidget.setRowCount(len(ridList))
        for index, rid in enumerate(ridList):
            item = UneditableTableWidgetItem(str(rid))
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(index, 0, item)
        self.modBatchReplies: List[QtNetwork.QNetworkReply] = modBatchRequest(
            self.naManager,
            ridList,
            partial(self.onTableModNameFinished, serverIndex),
            self.onTableModNameErrorOccured,
        )

    def onTableModNameFinished(self, currentServerModListIndex: int, replyIndex: int):
        if (
            self.serversModList is None
            or self.modBatchReplies[replyIndex].error()
            != QtNetwork.QNetworkReply.NetworkError.NoError
        ):
            return

        result = json.loads(
            bytes(self.modBatchReplies[replyIndex].readAll().data()).decode()
        )
        resultModList = [Mod(item) for item in result["data"]]
        ridNameMap: Dict[int, str] = {}
        for mod in resultModList:
            ridNameMap[mod.getResourceId()] = mod.getName()
        serverRidList = self.serversModList[currentServerModListIndex]["ridList"]
        sortedNameList = [
            ridNameMap[rid] for rid in serverRidList if rid in ridNameMap.keys()
        ]
        for index, name in enumerate(sortedNameList):
            index += MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST * replyIndex
            item = UneditableTableWidgetItem(name)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(index, 1, item)
        self.modBatchReplies[replyIndex].deleteLater()
        # del self.persistences["modBatchRequest"]

    def onTableModNameErrorOccured(
        self, replyIndex: int, error: QtNetwork.QNetworkReply.NetworkError
    ):
        InfoBar.error(
            title="无法获取搜索结果",
            content=error.name,
            position=InfoBarPosition.BOTTOM_RIGHT,
            parent=self,
        )
        self.modBatchReplies[replyIndex].deleteLater()
        # del self.persistences["modBatchRequest"]

    def initServerComboBox(self):
        self.ui.serverComboBox.setPlaceholderText("请选择一个服务器")
        request = QtNetwork.QNetworkRequest(QUrl(SERVERS_MOD_LIST_URL))
        self.serversModListReply = self.naManager.get(request)
        self.serversModListReply.finished.connect(self.onGetServersModListFinished)
        self.serversModListReply.errorOccurred.connect(
            self.onGetServersModListErrorOccurred
        )

    def onGetServersModListFinished(self):
        if (
            self.serversModListReply.error()
            != QtNetwork.QNetworkReply.NetworkError.NoError
        ):
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
    app.exec()
