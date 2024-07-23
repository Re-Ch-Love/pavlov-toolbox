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
        self._data = data

    @staticmethod
    def constructFromApi(resourceID: int) -> "ModData":
        """从Api中获取数据以构造ModData对象

        使用requests库获取数据，因此不能在主线程中执行。一般用于开发中的测试。

        Args:
            resourceID (int): Mod资源ID

        Raises:
            ModDataNotFound: 当Mod数据对象不存在时抛出

        Returns:
            ModData: 略
        """
        res = requests.get(
            f"https://api.pavlov-toolbox.rech.asia/modio/v1/games/@pavlov/mods?_limit=1&id={resourceID}"
        )
        res.raise_for_status()
        jsonObj = res.json()
        data = jsonObj["data"]
        if len(data) == 0:
            raise ModDataNotFound("Mod数据对象", modId=resourceID)
        return ModData(data[0])

    def getModFileLive(self, platformName: str) -> int:
        platform_list: List[Dict] = self._data["platforms"]
        for platform in platform_list:
            if platform["platform"] == platformName:
                return int(platform["modfile_live"])
        raise ModDataNotFound(f"目标平台", platformName=platformName, mod_raw_data=self._data)

    def getWindowsDownloadUrl(self) -> str:
        rid = self._data["id"]
        modFileLive = self.getModFileLive("windows")
        return f"https://g-3959.modapi.io/v1/games/3959/mods/{rid}/files/{modFileLive}/download"

    @property
    def taint(self) -> int:
        return self.getModFileLive("windows")

    @property
    def name(self) -> str:
        """Mod名称（只读）"""
        return self._data["name"]

    @property
    def resourceId(self) -> int:
        """Mod资源ID（只读）"""
        return self._data["id"]

    def __str__(self) -> str:
        return f"ModData(name={self.name}, resourceId={self.resourceId})"

    def __repr__(self) -> str:
        return f"ModData(name={self.name}, resourceId={self.resourceId})"


MOD_BATCH_REQUEST_URL = "https://api.pavlov-toolbox.rech.asia/modio/v1/games/@pavlov/mods?id-in=%s"
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
        currentGroup = modRidList[startIndex : startIndex + MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST]
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
    # 将请求分组，90个一组（太多了不能一次性请求，根据测试请求的上限应该是100个，保险起见90个一组）
    groups: List[str] = []
    for startIndex in range(0, len(ridList), 90):
        # 将rid用逗号连接
        ridParam = ",".join([str(rid) for rid in ridList[startIndex : startIndex + 100]])
        # 拼接目标url
        url = MOD_BATCH_REQUEST_URL % ridParam
        groups.append(url)

    def convertToModData(context: bytes, otherModDataList: List[ModData] | None = None):
        resultModList: List[ModData] = [ModData(data) for data in json.loads(context)["data"]]
        if otherModDataList:
            resultModList.extend(otherModDataList)
        if len(groups) != 0:
            return (
                QRequestReady(parent)
                .get(groups.pop())
                .then(partial(convertToModData, otherModDataList=resultModList))
            )
        return resultModList

    return QRequestReady(parent).get(groups.pop()).then(convertToModData)


def test1():
    ridList = [
        2771448,
        2773654,
        2773760,
        2788214,
        2788277,
        2790869,
        2802847,
        2804210,
        2804502,
        2809826,
        2810499,
        2811148,
        2811370,
        2812319,
        2813799,
        2817844,
        2829349,
        2840314,
        2840384,
        2844898,
        2849391,
        2856317,
        2867687,
        2871454,
        2879562,
        2996823,
        3002208,
        3002600,
        3018770,
        3020535,
        3037601,
        3048982,
        3051820,
        3054096,
        3054923,
        3061028,
        3084806,
        3084882,
        3085188,
        3090639,
        3094680,
        3094925,
        3104159,
        3106258,
        3113040,
        3113360,
        3116397,
        3116594,
        3122797,
        3126365,
        3131146,
        3132480,
        3133545,
        3173315,
        3173489,
        3188315,
        3189342,
        3193506,
        3223142,
        3223861,
        3231288,
        3231764,
        3237514,
        3243988,
        3265534,
        3268798,
        3269828,
        3269978,
        3270138,
        3270182,
        3302201,
        3370978,
        3391413,
        3391531,
        3395364,
        3462586,
        3463467,
        3467755,
        3484154,
        3534001,
        3541450,
        3556047,
        3564015,
        3664797,
        3698400,
        3748215,
        3754271,
        3785974,
        3798700,
        3901501,
        3924157,
        3927308,
        3936882,
        3943563,
        3943838,
        3945378,
        3951597,
        3953175,
        3965340,
        3969882,
        3975268,
        3977264,
        4006655,
        4009773,
        4075563,
        4113442,
        4128088,
        4136968,
    ]
    print(len(set(ridList)))
    # ridList = [mod.resourceId for mod in getLocalMods()]
    app = QApplication()
    (
        modBatchQRequest(app, ridList).then(lambda mods: print(len(mods)))
        # .then(lambda mods: print([mod.name for mod in mods]))
        .done()
    )
    app.exec()


if __name__ == "__main__":
    test1()
