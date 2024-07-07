from typing import List
from features.common.mod_installation import CardName
from features.common.mod import ModData
from features.search.common import SearchMode
from features.search.model import SearchModel
from features.common.globals_objects import Globals

class SearchPresenter:

    def __init__(self, view) -> None:
        # 这个import不能放到文件顶部，否则会因为循环依赖导致报错
        from features.search.view import SearchView

        self.view: SearchView = view
        self.model = SearchModel()

    def search(self, input: str):
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

    def install(self, url: str, modName: str):
        Globals.modInstallationManager.addJob([url], CardName(modName, ""))
