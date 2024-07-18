from functools import partial
import json
from PySide6 import QtNetwork
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication
from qfluentwidgets import QObject
import requests
from typing import Callable, Dict, List

from common.qrequest import QRequestReady


class ModDataNotFound(Exception):
    def __init__(self, data_name: str, **kwargs) -> None:
        self.data_name = data_name
        self.kwargs = kwargs

    def __str__(self) -> str:
        return f"`{self.data_name}`未找到。附加信息：{self.kwargs}"


# Taint文件内容是mod.getModFileLive("windows")
class ModData:
    def __init__(self, data: dict) -> None:
        self.data = data

    @staticmethod
    def constructFromServer(resourceID: int):
        res = requests.get(
            f"https://api.pavlov-toolbox.rech.asia/modio/v1/games/@pavlov/mods?_limit=1&id={resourceID}"
        )
        res.raise_for_status()
        jsonObj = res.json()
        data = jsonObj["data"]
        if len(data) == 0:
            raise ModDataNotFound("mod数据对象", modId=resourceID)
        return ModData(data[0])

    def getModFileLive(self, platformName: str) -> int:
        platform_list: List[Dict] = self.data["platforms"]
        for platform in platform_list:
            if platform["platform"] == platformName:
                return int(platform["modfile_live"])
        raise ModDataNotFound(
            f"目标平台", platformName=platformName, mod_raw_data=self.data
        )

    def getWindowsDownloadUrl(self) -> str:
        rid = self.data["id"]
        modFileLive = self.getModFileLive("windows")
        return f"https://g-3959.modapi.io/v1/games/3959/mods/{rid}/files/{modFileLive}/download"

    @property
    def name(self) -> str:
        """Mod名称（只读）"""
        return self.data["name"]

    @property
    def resourceId(self) -> int:
        """Mod资源ID（只读）"""
        return self.data["id"]

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return str(self.data)


MOD_BATCH_REQUEST_URL = (
    "https://api.pavlov-toolbox.rech.asia/modio/v1/games/@pavlov/mods?id-in=%s"
)
# 批量请求时，每一次请求的最大Mod数量
MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST = 50


def modBatchRequest(
    naManager: QtNetwork.QNetworkAccessManager,
    modRidList: List[int],
    onFinished: Callable[[int], None],
    onErrorOccurred: Callable[[int, QtNetwork.QNetworkReply.NetworkError], None],
) -> List[QtNetwork.QNetworkReply]:
    """
    批量处理MOD请求。

    使用分批请求策略，将大量的MOD ID分组，每个分组不超过MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST个ID，
    然后对每个分组发送一个网络请求。这样可以避免一次性发送过多请求导致的网络问题或服务器压力。

    参数:
    naManager: QNetworkAccessManager对象，用于发送网络请求。
    modRidList: 包含所有MOD ID的列表。
    onFinished: 请求成功完成时调用的回调函数，接收一个参数表示对应的reply的索引。（例如索引为0则说明这是modRidList中第1个
    onErrorOccurred: 请求发生错误时调用的回调函数，接收两个参数，分别是发生错误的reply的索引和错误类型。

    返回:
    包含所有发送的网络请求的回复对象列表。

    使用方法：
    ```
    class Foo:
        def request(self):
            self.replies = modBatchRequest(...)
        def onFinished(self, replyIndex):
            if self.modBatchReplies[replyIndex].error()
                != QtNetwork.QNetworkReply.NetworkError.NoError:
                return
            # 处理replyIndex对应的reply
            ...
            self.replies[replyIndex].deleteLater()
        def onErrorOccurred(self, replyIndex, error):
            # 处理replyIndex对应的reply
            ...
            self.replies[replyIndex].deleteLater()
    ```
    """
    # 一次不能请求太多，把数据按GROUP_MAX分组后再分别请求
    replies: List[QtNetwork.QNetworkReply] = []
    for replyIndex, startIndex in enumerate(
        range(0, len(modRidList), MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST)
    ):
        currentGroup = modRidList[
            startIndex : startIndex + MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST
        ]
        # 把rid用逗号连接
        ids = ",".join([str(rid) for rid in currentGroup])
        request = QtNetwork.QNetworkRequest(QUrl(MOD_BATCH_REQUEST_URL % ids))
        reply = naManager.get(request)
        reply.finished.connect(partial(onFinished, replyIndex))
        reply.errorOccurred.connect(partial(onErrorOccurred, replyIndex))
        replies.append(reply)
    return replies


def modBatchQRequest(parent: QObject, ridList: List[int]):
    """使用QRequest批量处理MOD数据请求"""
    # 将rid用逗号连接
    ridParam = ",".join([str(rid) for rid in ridList])
    # 获取请求url
    url = MOD_BATCH_REQUEST_URL % ridParam

    def splitModData(context: bytes):
        return [ModData(data) for data in json.loads(context)["data"]]

    return QRequestReady(parent).get(url).then(splitModData)


if __name__ == "__main__":
    ridList = [
        3462586,
        3467755,
        3269978,
        3270138,
        3798700,
        3484154,
        3953175,
        3943563,
        3969882,
        3268798,
        3391531,
        3391413,
        4009773,
        3977264,
        3020535,
        2996823,
        3051820,
        3223861,
        3116594,
        2867687,
        2856317,
        3173315,
        3265534,
        3231288,
        3624316,
        3188315,
        3002208,
        3048982,
        3061028,
        3054923,
        4115864,
        4118866,
        4075563,
        2802847,
        2813799,
        2771448,
        2803451,
        3084806,
        3116397,
        2811370,
        2810499,
        3252855,
        3090639,
        2790869,
        3104159,
        3106258,
        3113360,
        3037601,
        2773760,
        3113040,
        2970978,
        3252313,
        2849391,
        4045141,
    ]
    print(len(set(ridList)))
    app = QApplication()
    (
        modBatchQRequest(app, ridList)
        .then(lambda mods: print(len(mods)))
        # .then(lambda mods: print([mod.name for mod in mods]))
        .done()
    )
    app.exec()
