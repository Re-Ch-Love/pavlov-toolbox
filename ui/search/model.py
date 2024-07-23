import json
from typing import Callable, List
from PySide6 import QtNetwork
from PySide6.QtCore import QUrl
import urllib.parse

from qfluentwidgets import QObject

from common.mod.mod_data import ModData
from common.qrequest import QRequestReady
from ui.search.search_mod import SearchMode

SEARCH_LIMIT = 10


class SearchModel:

    def __init__(self) -> None:
        self.searchMode = SearchMode.modName
        self.naManager = QtNetwork.QNetworkAccessManager()

    def search(
        self,
        input: str,
        parent: QObject,
        finishCallback: Callable[[List[ModData]], None],
        errorCallback: Callable[[str], None],
    ):
        if input.strip() == "":
            return
        if self.searchMode == SearchMode.modName:
            url = f"https://api.pavlov-toolbox.rech.asia/modio/v1/games/@pavlov/mods?_limit={SEARCH_LIMIT}&_sort=-popular&_q={urllib.parse.quote(input)}"
        elif self.searchMode == SearchMode.rid:
            url = f"https://api.pavlov-toolbox.rech.asia/modio/v1/games/@pavlov/mods?_limit=1&id={urllib.parse.quote(input)}"
        else:
            raise RuntimeError("Unknown search mode")

        def onFinish(content):
            resultDict = json.loads(content)
            mods = [ModData(itemData) for itemData in resultDict["data"]]
            finishCallback(mods)

        (
            QRequestReady(parent)
            .get(url)
            .then(onFinish)
            .catch(lambda err: errorCallback(err.name))
            .done()
        )
