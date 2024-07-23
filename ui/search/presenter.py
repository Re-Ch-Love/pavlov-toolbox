from typing import List

from common.mod.local_mods import LocalModInfo, retrieveLocalMods, retrieveModsStatusInLocal
from common.mod.mod_data import ModData
from common.mod.installation.mod_download_manager import ModDownloadManager
from ui.search.search_mod import SearchMode
from ui.search.model import SearchModel


class SearchPresenter:

    def __init__(self, view) -> None:
        # 这个import不能放到文件顶部，否则会因为循环依赖导致报错
        from ui.search.view import SearchView

        self.view: SearchView = view
        self.model = SearchModel()

    def search(self, input: str):

        def onSearchFinish(modDataList: List[ModData]):
            if len(modDataList) == 0:
                self.view.promptNoSearchResult()
                return
            localMods = retrieveLocalMods()
            modStatusInLocalList = retrieveModsStatusInLocal(modDataList, localMods)
            self.view.showResult(modDataList, modStatusInLocalList)

        def onSearchError(reason):
            self.view.promptSearchError(reason)

        self.model.search(input, self.view, onSearchFinish, onSearchError)

    def setSearchMode(self, mode: SearchMode):
        self.model.searchMode = mode

    def install(self, modData: ModData):
        ModDownloadManager.getInstance().addTask(modData)
