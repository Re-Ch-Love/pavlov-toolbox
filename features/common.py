from functools import partial
from PySide6 import QtNetwork
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QTableWidgetItem
import requests
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar
from qfluentwidgets import MessageBox

class TargetNotFound(Exception):
    def __init__(self, data_name: str, **kwargs) -> None:
        self.data_name = data_name
        self.kwargs = kwargs

    def __str__(self) -> str:
        return f"`{self.data_name}`未找到。附加信息：{self.kwargs}"

# Taint文件内容是mod.getModFileLive("windows")
class Mod:
    def __init__(self, data: dict) -> None:
        self.data = data
    
    @staticmethod
    def constructFromServer(modId: int):
        res = requests.get(
            f"https://api.pavlov-toolbox.rech.asia/modio/v1/games/@pavlov/mods?_limit=1&id={modId}",
        )
        res.raise_for_status()
        data = res.json()["data"]
        if len(data) == 0:
            raise TargetNotFound("mod数据对象", modId=modId)
        return Mod(data[0])

    def getModFileLive(self, platformName: str) -> str:
        platform_list: List[Dict] = self.data["platforms"]
        for platform in platform_list:
            if platform["platform"] == platformName:
                return str(platform["modfile_live"])
        raise TargetNotFound(f"目标平台", platformName=platformName, mod_raw_data=self.data)

    def getWindowsDownloadUrl(self) -> str:
        return f"https://g-3959.modapi.io/v1/games/3959/mods/{self.data['id']}/files/{self.getModFileLive("windows")}/download"
    
    def getName(self) -> str:
        return self.data["name"]

    def getResourceId(self) -> int:
        return self.data["id"]


MOD_BATCH_REQUEST_URL = "https://api.pavlov-toolbox.rech.asia/modio/v1/games/@pavlov/mods?id-in=%s"
# 批量请求时，每一次请求的最大Mod数量
MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST = 50

def modBatchRequest(naManager: QtNetwork.QNetworkAccessManager, modRidList: List[int], onFinished: Callable[[int], None], onErrorOccurred: Callable[[int, QtNetwork.QNetworkReply.NetworkError], None]):
    # 一次不能请求太多，把数据按GROUP_MAX分组后再分别请求
    replies = []
    for replyIndex, startIndex in enumerate(range(0, len(modRidList), MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST)):
        currentGroup = modRidList[startIndex:startIndex+MOD_BATCH_REQUEST_MAX_MODS_PER_REQUEST]
        # 把rid用逗号连接
        ids = ",".join([str(rid) for rid in currentGroup])
        request = QtNetwork.QNetworkRequest(QUrl(MOD_BATCH_REQUEST_URL % ids))
        reply = naManager.get(request)
        reply.finished.connect(partial(onFinished, replyIndex))
        reply.errorOccurred.connect(partial(onErrorOccurred, replyIndex))
        replies.append(reply)
    return replies
        

class ChineseMessageBox(MessageBox):
    def __init__(self, title: str, content: str, parent):
        super().__init__(title, content, parent)
        self.yesButton.setText("确定")
        self.cancelButton.setText("取消")

# 大写开头是因为该函数模拟了一个继承的行为，所以将它当作一个类来看待
def UneditableTableWidgetItem(content: str):
    item = QTableWidgetItem(content)
    item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
    return item

def calculateProgresssPercentage(completedLength: int, totalLength: int, n: int) -> float:
    """返回下载进度百分比，保留`n`位小数，取值范围[0, 1]，如果`totalLength`为0则返回0.0"""
    if totalLength != 0:
        percentage = round(completedLength / totalLength, n)
    else:
        percentage = 0.0
    return percentage

def byteLengthToHumanReadable(bytes: int):
    """将字节长度转化为人类可读的形式，返回一个元组`(数量，单位)`"""
    if bytes >= 1024 * 1024:
        number = round(bytes / 1024 / 1024, 2)
        unit = "MB"
    elif bytes >= 1024:
        number = round(bytes / 1024, 2)
        unit = "KB"
    else:
        number = bytes
        unit = "B"
    return number, unit

_T = TypeVar('_T')

def defaultIfNone(obj: Optional[_T], default: _T) -> _T:
    return default if obj is None else obj

# def doIfdifferent(obj1: Any, obj2: Any, func: Callable[[], _T]) -> _T | None:
#     return func() if obj1 != obj2 else None

if __name__ == "__main__":
    print(calculateProgresssPercentage(128, 1000, 3))