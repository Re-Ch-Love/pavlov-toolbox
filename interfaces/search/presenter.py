from typing import List

from common.mod.local_mods import LocalModInfo, getLocalMods
from common.mod.mod_data import ModData
from common.mod.mod_installation import ModInstallationManager
from interfaces.search.common import SearchMode
from interfaces.search.model import SearchModel


class SearchPresenter:

    def __init__(self, view) -> None:
        # 这个import不能放到文件顶部，否则会因为循环依赖导致报错
        from interfaces.search.view import SearchView

        self.view: SearchView = view
        self.model = SearchModel()
        self.localMods: List[LocalModInfo]

    def search(self, input: str):
        self.localMods = getLocalMods()

        def onSearchFinish(mods: List[ModData]):
            if len(mods) == 0:
                self.view.promptNoSearchResult()
                return
            self.view.showResult(mods)

        def onSearchError(reason):
            self.view.promptSearchError(reason)

        self.model.search(input, onSearchFinish, onSearchError)

    def setSearchMode(self, mode: SearchMode):
        self.model.searchMode = mode

    def install(self, modData: ModData):
        ModInstallationManager.getInstance().addJob(modData)

    def getActionButtonText(self, modData: ModData):
        localModRids = [localMod.resourceId for localMod in self.localMods]
        if modData.resourceId in localModRids:
            matchedLocalMod = next(
                (localMod for localMod in self.localMods if localMod.resourceId == modData.resourceId)
            )
            if matchedLocalMod.taint == modData.getModFileLive("windows"):
                return "已安装"
            else:
                return "更新"
        else:
            return "安装"
