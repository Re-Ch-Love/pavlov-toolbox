from functools import partial
from PySide6 import QtNetwork
from PySide6.QtCore import QUrl
import requests
from typing import Callable, Dict, List


class ModInfoNotFound(Exception):
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
            f"https://api.pavlov-toolbox.rech.asia/modio/v1/games/@pavlov/mods?_limit=1&id={resourceID}",
        )
        res.raise_for_status()
        data = res.json()["data"]
        if len(data) == 0:
            raise ModInfoNotFound("mod数据对象", modId=resourceID)
        return ModData(data[0])

    def getModFileLive(self, platformName: str) -> int:
        platform_list: List[Dict] = self.data["platforms"]
        for platform in platform_list:
            if platform["platform"] == platformName:
                return int(platform["modfile_live"])
        raise ModInfoNotFound(f"目标平台", platformName=platformName, mod_raw_data=self.data)

    def getWindowsDownloadUrl(self) -> str:
        return f"https://g-3959.modapi.io/v1/games/3959/mods/{self.data['id']}/files/{self.getModFileLive("windows")}/download"

    def getName(self) -> str:
        return self.data["name"]

    def getResourceId(self) -> int:
        return self.data["id"]


MOD_BATCH_REQUEST_URL = "https://api.pavlov-toolbox.rech.asia/modio/v1/games/@pavlov/mods?id-in=%s"
# 批量请求时，每一次请求的最大Mod数量
MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST = 50


def modBatchRequest(naManager: QtNetwork.QNetworkAccessManager, modRidList: List[int],
                    onFinished: Callable[[int], None],
                    onErrorOccurred: Callable[[int, QtNetwork.QNetworkReply.NetworkError], None]) -> List[QtNetwork.QNetworkReply]:
    """
    批量处理MOD请求。

    使用分批请求策略，将大量的MOD ID分组，每个分组不超过MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST个ID，
    然后对每个分组发送一个网络请求。这样可以避免一次性发送过多请求导致的网络问题或服务器压力。

    参数:
    naManager: QNetworkAccessManager对象，用于发送网络请求。
    modRidList: 包含所有MOD ID的列表。
    onFinished: 请求成功完成时调用的回调函数，接收一个参数表示发生错误的reply的索引。（例如索引为0则说明这是modRidList中第1个
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
    for replyIndex, startIndex in enumerate(range(0, len(modRidList), MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST)):
        currentGroup = modRidList[startIndex:startIndex + MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST]
        # 把rid用逗号连接
        ids = ",".join([str(rid) for rid in currentGroup])
        request = QtNetwork.QNetworkRequest(QUrl(MOD_BATCH_REQUEST_URL % ids))
        reply = naManager.get(request)
        reply.finished.connect(partial(onFinished, replyIndex))
        reply.errorOccurred.connect(partial(onErrorOccurred, replyIndex))
        replies.append(reply)
    return replies
