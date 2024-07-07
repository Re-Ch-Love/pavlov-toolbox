import json
from typing import Callable, List
from PySide6 import QtNetwork
from PySide6.QtCore import QUrl
from features.common.mod import ModData
from features.search.common import SearchMode
import urllib.parse

SEARCH_LIMIT = 10


class SearchModel:

    def __init__(self) -> None:
        self.searchMode = SearchMode.modName
        self.naManager = QtNetwork.QNetworkAccessManager()

    def search(
        self,
        input: str,
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
            raise Exception("Unknown search mode")
        self.searchFinishCallback = finishCallback
        self.searchErrorCallback = errorCallback
        request = QtNetwork.QNetworkRequest(QUrl(url))
        self.searchReply = self.naManager.get(request)
        self.searchReply.finished.connect(self.onSearchFinished)
        self.searchReply.errorOccurred.connect(self.onSearchErrorOccured)

    def onSearchErrorOccured(self, error: QtNetwork.QNetworkReply.NetworkError):
        self.searchErrorCallback(error.name)
        self.searchReply.deleteLater()

    def onSearchFinished(self):
        if (
            error := self.searchReply.error()
        ) != QtNetwork.QNetworkReply.NetworkError.NoError:
            self.searchErrorCallback(error.name)
            return
        rawResult = bytes(self.searchReply.readAll().data()).decode()
        resultDict = json.loads(rawResult)
        mods = [ModData(itemData) for itemData in resultDict["data"]]
        self.searchFinishCallback(mods)
        self.searchReply.deleteLater()
