from functools import partial
import json
from typing import Callable, List
from typing_extensions import deprecated
from PySide6 import QtNetwork
from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply
from PySide6.QtWidgets import QApplication
from qfluentwidgets import QObject

from features.common.mod import MOD_BATCH_REQUEST_URL, ModData, modBatchRequest
from features.common.qrequest import QDataPromise, QPromise, QRequestPromise, QRequestReady


DEPENDENCIES_URL = "https://api.pavlov-toolbox.rech.asia/modio/v1/games/3959/mods/%d/dependencies?recursive=true"

class ModDependenciesProcessor(QObject):
    """
    获取Mod依赖
    """

    def __init__(
        self,
        modData: ModData,
        finishCallback: Callable[[ModData, List[ModData]], None],
        errorCallback: Callable[[ModData, str], None],
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self.naManager = QNetworkAccessManager(self)
        self.finishCallback = finishCallback
        self.errorCallback = errorCallback
        self.modData = modData
        url = QUrl(DEPENDENCIES_URL % modData.getResourceId())
        request = QtNetwork.QNetworkRequest(url)
        self.reply = self.naManager.get(request)
        self.reply.finished.connect(self.onFinished)
        self.reply.errorOccurred.connect(self.onErrorOccurred)
        self.modDataList: List[ModData] = []
        self.modDataReceivedCount = 0

    def onFinished(self) -> None:
        if self.reply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
            return
        content = bytes(self.reply.readAll().data()).decode()
        jsonObj = json.loads(content)
        if jsonObj["result_total"] == 0:
            self.finishCallback(self.modData, list())
        else:
            data = jsonObj["data"]
            ridList: List[int] = [item["mod_id"] for item in data]
            # 因为获取依赖Mod时返回的数据格式，与获取Mod的不一样，所以这里需要收集rid再请求一次
            self.modDataReplies = modBatchRequest(
                self.naManager, ridList, self.modDataFinished, self.modDataErrorOccurred
            )
        self.reply.deleteLater()

    def onErrorOccurred(self, error: QtNetwork.QNetworkReply.NetworkError) -> None:
        self.errorCallback(self.modData, error.name)
        self.reply.deleteLater()

    def modDataFinished(self, replyIndex: int):
        self.modDataReceivedCount += 1
        reply = self.modDataReplies[replyIndex]
        if reply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
            return
        content = bytes(reply.readAll().data()).decode()
        jsonObj = json.loads(content)
        for item in jsonObj["data"]:
            self.modDataList.append(ModData(item))
        if self.modDataReceivedCount == len(self.modDataReplies):
            self.finishCallback(self.modData, self.modDataList)

    def modDataErrorOccurred(self, replyIndex: int, error: QNetworkReply.NetworkError):
        # 暂时不处理获取失败的情况
        pass


def getModDependencies(request: QRequestReady, rid: int) -> QPromise:
    def getDependencies(content: bytes) -> List[int]:
        jsonObj = json.loads(content)
        if jsonObj["result_total"] == 0:
            return []
        else:
            data = jsonObj["data"]
            # 因为获取依赖Mod时返回的数据格式，与获取Mod的不一样，所以这里需要用rid再请求一次
            return [item["mod_id"] for item in data]
    def dependenciesToModData(rids: List[int] | None) -> QPromise:
        nonlocal request
        if not rids:
            return QDataPromise([])
        else:
            ridsParam = ",".join([str(rid) for rid in rids])
            return (
                request.get(MOD_BATCH_REQUEST_URL % ridsParam)
                    .then(lambda content: [ModData(item) for item in json.loads(content)["data"]])
            )
        
    return (request.get(DEPENDENCIES_URL % rid)
            .then(getDependencies)
            .then(dependenciesToModData))

        


if __name__ == "__main__":
    app = QApplication()
    modList = [
        3061028,
        3048982,
        3116594,
        3094680,
        3243988,
        3002600,
        3020535,
        3002208,
        2996823,
        3051820,
        2804502,
        2879562,
        2867687,

        # 2871454,
        # 3265534,
        # 2856317,
        # 3467755,
        # 3924157,
        # 3975268,
        # 3268798,
        # 3943563,
        # 3969882,
        # 3901501,
    ]

    # def onFinish(modData: ModData, dependencies: List[ModData]):
    #     print(modData.getResourceId(), dependencies)

    # def onError(modData: ModData, reason: str):
    #     print(modData.getResourceId(), f"error: {reason}")

    # for rid in modList:
    #     ModDependenciesProcessor(
    #         ModData.constructFromServer(rid), onFinish, onError, app
    #     )

    # 3243988 有依赖
    (
        getModDependencies(QRequestReady(app), 3243988)
            .then(lambda modDataList: print([modData.getResourceId() for modData in modDataList]))
            .done()
    )
    app.exec()
