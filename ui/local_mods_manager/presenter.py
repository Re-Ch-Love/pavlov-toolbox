from ast import Mod
from typing import List, Tuple
from common.log import AppLogger, logThis
from common.mod.local_mods import ModStatusInLocal, retrieveLocalMods, retrieveModsStatusInLocal
from common.mod.mod_data import ModData, modBatchQRequest
from common.mod.installation.mod_download_manager import ModDownloadManager


class LocalModsManagerPresenter:
    def __init__(self, view) -> None:
        from ui.local_mods_manager.view import LocalModsManagerView

        self.view: LocalModsManagerView = view
        self.lastTableData: Tuple[List[ModData], List[ModStatusInLocal]] | None = None

    def loadMods(self):
        localMods = retrieveLocalMods()
        
        def compareVersionAndShow(modDataList: List[ModData]):
            modStatusInLocalList = retrieveModsStatusInLocal(modDataList, localMods)
            self.lastTableData = (modDataList, modStatusInLocalList)
            self.view.loadModTable(modDataList, modStatusInLocalList)

        modBatchQRequest(self.view, [mod.resourceId for mod in localMods]).then(
            compareVersionAndShow
        ).done()

    def install(self, modData: ModData):
        self.view.showInstallMsg()
        ModDownloadManager.getInstance().addTask(modData)

    def installAll(self):
        if self.lastTableData is None:
            AppLogger().warning("lastTableData is None")
            return
        self.view.disableAllButton()
        self.view.showInstallMsg()
        modDownloadManager = ModDownloadManager.getInstance()
        for mod, modStatusInLocal in zip(*self.lastTableData):
            if modStatusInLocal == ModStatusInLocal.OUTDATED:
                modDownloadManager.addTask(mod)
