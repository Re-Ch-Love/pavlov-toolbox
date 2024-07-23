import json
from typing import Any, Dict, Optional, cast

from PySide6 import QtNetwork
from qfluentwidgets import List, PushButton
from common.log import AppLogger
from common.mod.local_mods import ModStatusInLocal, retrieveLocalMods, retrieveModsStatusInLocal
from common.mod.mod_data import ModData, modBatchQRequest
from common.mod.installation.mod_download_manager import ModDownloadManager
from common.qrequest import QRequestReady

SERVERS_MOD_LIST_URL = "https://api.pavlov-toolbox.rech.asia/servers-mod-list"


class ServerModPresenter:
    def __init__(self, view) -> None:
        from ui.server_mod.view import ServerModView

        self.view: ServerModView = view
        self.serversModList: List[Dict[str, Any]] = []
        self.selectedMods: List[ModData] = []
        self.modStatusInLocalList: List[ModStatusInLocal] = []

    def loadModTable(self, index):
        localMods = retrieveLocalMods()
        self.selectedMods.clear()

        def processAndShowResult(modDataList: List[ModData]):
            self.selectedMods = modDataList
            self.modStatusInLocalList = retrieveModsStatusInLocal(modDataList, localMods)
            self.view.showMods(self.selectedMods, self.modStatusInLocalList)

        (
            modBatchQRequest(self.view, self.serversModList[index]["ridList"])
            .then(processAndShowResult)
            .done()
        )

    def loadServersModList(self):
        def processAndShowResult(content: bytes):
            self.serversModList = json.loads(content)
            if self.serversModList is None:
                AppLogger().warning("serversModList is None after loads json from api")
                return
            nameList = [obj["serverName"] for obj in self.serversModList]
            self.view.showServersModList(nameList)

        def catchError(error: QtNetwork.QNetworkReply.NetworkError):
            self.view.showNetworkErrorInfo(error)

        (
            QRequestReady(self.view)
            .get(SERVERS_MOD_LIST_URL)
            .then(processAndShowResult)
            .catch(catchError)
            .done()
        )

    def installMod(self, button: PushButton, modData: ModData):
        self.view.showAddJobInfo()
        button.setText("安装中")
        button.setEnabled(False)
        ModDownloadManager.getInstance().addTask(modData)

    def installAllMod(self):
        self.view.disableAllButtonInTable()
        self.view.showAddJobInfo()
        for modData, modStatusInLocal in zip(self.selectedMods, self.modStatusInLocalList):
            if modStatusInLocal != ModStatusInLocal.INSTALLED_AND_LATEST:
                ModDownloadManager.getInstance().addTask(modData)
