from typing import List
from features.common.local_mods import LocalModInfo, getLocalMods
from features.common.mod_installation import CardName, ModInstallationManager
from features.common.mod import ModData
from features.search.common import SearchMode
from features.search.model import SearchModel
from features.common.global_objects import Globals


class SearchPresenter:

    def __init__(self, view) -> None:
        # 这个import不能放到文件顶部，否则会因为循环依赖导致报错
        from features.search.view import SearchView

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
        localModRids = [localMod.rid for localMod in self.localMods]
        if modData.getResourceId() in localModRids:
            matchedLocalMod = next(
                (
                    localMod
                    for localMod in self.localMods
                    if localMod.rid == modData.getResourceId()
                )
            )
            if matchedLocalMod.taint == modData.getModFileLive("windows"):
                return "已安装"
            else:
                return "更新"
        else:
            return "安装"
