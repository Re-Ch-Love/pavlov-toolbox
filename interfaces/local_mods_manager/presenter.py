from typing import List, Tuple
from common.mod.local_mods import getLocalMods
from common.mod.mod_data import ModData, modBatchQRequest
from common.mod.mod_installation import ModInstallationManager


class LocalModsManagerPresenter:
    def __init__(self, view) -> None:
        from interfaces.local_mods_manager.view import LocalModsManagerView

        self.view: LocalModsManagerView = view
        self.lastTableData: List[Tuple[ModData, bool]] = []

    def loadMods(self):
        localMods = getLocalMods()
        localModRidList = [mod.resourceId for mod in localMods]

        def compareVersionAndSHow(mods: List[ModData]):
            # 遍历localMods列表，找到匹配的modData
            for localMod in localMods:
                # 找到匹配的modData
                matchedModData = next(
                    (mod for mod in mods if mod.resourceId == localMod.resourceId)
                )
                # 如果taint不相等，说明不是最新版
                if localMod.taint != matchedModData.getModFileLive("windows"):
                    self.lastTableData.append((matchedModData, False))
                else:
                    self.lastTableData.append((matchedModData, True))
            self.view.loadModTable(self.lastTableData)

        modBatchQRequest(self.view, localModRidList).then(compareVersionAndSHow).done()

    def install(self, modData: ModData):
        self.view.showInstallMsg()
        ModInstallationManager.getInstance().addJob(modData)

    def installAll(self):
        self.view.disableAllButton()
        self.view.showInstallMsg()
        for mod, isLatest in self.lastTableData:
            if not isLatest:
                ModInstallationManager.getInstance().addJob(mod)
