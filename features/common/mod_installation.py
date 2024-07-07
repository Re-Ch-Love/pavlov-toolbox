import collections
from enum import Enum
import json
import os
import random
import time
from typing import Callable, List, NamedTuple
from uuid import uuid4

from PySide6 import QtNetwork
from PySide6.QtNetwork import QNetworkAccessManager
from PySide6.QtWidgets import QApplication
from qfluentwidgets import QObject
from aria2.aria2 import Aria2
from features.common.decorators import cached
from features.common.download_info import DownloadInfo
from features.common.mod import ModData, modBatchRequest


class ModInstallationStage(Enum):
    """安装阶段，主要分为下载、解压和移动到Mod安装目录三个阶段"""

    downloading = 1
    importing = 2
    succeed = 3
    error = 4


class CardName(NamedTuple):
    displayName: str
    hintName: str


aria2 = Aria2()
aria2.startRpcServer()


class ModInstallationJob:
    """
    表示Mod安装工作的类

    只需要不停的调用（例如间隔1s）其update()方法，即可刷新阶段信息。
    在调用update前，即使前一个阶段的工作已经完成，也不会进入下一个阶段。（只有调用update()时才会检测当前阶段是否完成）

    stage为error时，errorReason字段表示错误原因
    """

    def __init__(
        self, gid: str, cardName: CardName, modInstallationDirPath: str
    ) -> None:
        """
        参数 `urls`：内容为相同资源的url列表（可以只传入一个）
        """
        self.gid = gid
        self.stage = ModInstallationStage.downloading
        self.cardName = cardName
        self.downloadInfo = DownloadInfo()
        self.modInstallationDirPath = modInstallationDirPath
        self.errorReason: str = ""

    def update(self):
        match self.stage:
            case ModInstallationStage.downloading:
                self._updateDownloadInfo()
                # TODO 补全其它状态信息
                if self.downloadInfo.status == "complete":
                    self.stage = ModInstallationStage.importing
            case ModInstallationStage.importing:
                self._updateImportStatus()
            case ModInstallationStage.succeed:
                pass  # 不做处理
            case ModInstallationStage.error:
                pass  # 不做处理

    def _updateDownloadInfo(self):
        raw = aria2.tellStatus(self.gid, DownloadInfo.ARIA2_RPC_KEYS)
        info = DownloadInfo()
        info.loadFromAria2RawData(raw["result"])
        self.downloadInfo = info

    def _updateImportStatus(self):
        pass


class MockModInstallationJob(ModInstallationJob):
    """
    模拟ModInstallationJob，用于测试界面
    """

    def __init__(self) -> None:
        self.gid = str(uuid4())
        self.stage = ModInstallationStage.downloading
        self.cardName = CardName(f"模拟数据{self.gid[:6]}", self.gid)
        self.downloadInfo = DownloadInfo()
        self.modInstallationDirPath = ""
        self.errorReason: str = ""

        # 随机3s-10s后下载完成
        self.endDownloadingTime = time.time() + random.randint(3, 10)
        # 下载完成后，随机1s-5s后导入完成
        self.endImportingTime = self.endDownloadingTime + random.randint(1, 5)

    def update(self):
        match self.stage:
            case ModInstallationStage.downloading:
                if time.time() > self.endDownloadingTime:
                    # print(f"{self.gid[:6]} enter importing stage")
                    self.stage = ModInstallationStage.importing
            case ModInstallationStage.importing:
                if time.time() > self.endImportingTime:
                    # print(f"{self.gid[:6]} enter succeed stage")
                    self.stage = ModInstallationStage.succeed
            case ModInstallationStage.succeed:
                pass  # 不做处理
            case ModInstallationStage.error:
                pass  # 不做处理


class ModInstallationManager:
    def __init__(self) -> None:
        self._jobs: List[ModInstallationJob] = []

    def addJob(self, uris: List[str], cardName: CardName):
        gid = aria2.addUri(uris)
        job = ModInstallationJob(gid, cardName, "")
        self._jobs.append(job)
        return job

    def addMockJob(self, count: int):
        for _ in range(count):
            self._jobs.append(MockModInstallationJob())

    def updateAllJobs(self):
        for job in self._jobs:
            job.update()
            if job.stage == ModInstallationStage.succeed:
                self._jobs.remove(job)

    def getAllJobs(self):
        self.updateAllJobs()
        return self._jobs


class ModInstallationDirException(Exception):
    """Mod安装目录相关异常"""

    def __init__(self, details: str) -> None:
        super().__init__(details)


INI_MOD_DIR_SUFFIX = "ModDirectory="
GAME_SETTING_PATH_BEHIND_HOME = (
    r"AppData\Local\Pavlov\Saved\Config\Windows\GameUserSettings.ini"
)


@cached
def getModInstallationDir() -> str:
    """获取Mod安装目录"""
    homePath = os.path.expanduser("~")
    gameUserSettingsPath = os.path.join(homePath, GAME_SETTING_PATH_BEHIND_HOME)
    if not os.access(gameUserSettingsPath, os.F_OK | os.R_OK):
        raise ModInstallationDirException("文件不存在或无法访问")
    with open(gameUserSettingsPath, "r", encoding="utf-8") as f:
        for line in f:
            if not line.startswith(INI_MOD_DIR_SUFFIX):
                continue
            modDir = line[len(INI_MOD_DIR_SUFFIX) :].strip()
            return modDir
    raise ModInstallationDirException("无法找到Mod安装目录配置项")


class LocalModInfo(NamedTuple):
    rid: int
    taint: int


class ModDownloadInfo(NamedTuple):
    rid: int
    url: str


def getLocalMods():
    installationDir = getModInstallationDir()
    modPaths: List[LocalModInfo] = []
    for modDirName in os.listdir(installationDir):
        modDirFullPath = os.path.join(installationDir, modDirName)
        if not os.path.isdir(modDirFullPath):
            continue
        if not modDirName.startswith("UGC"):
            continue
        # 去除开头的UGC就是RID
        rid = int(modDirName[len("UGB") :])
        taintPath = os.path.join(modDirFullPath, "taint")
        with open(taintPath, "r") as f:
            taint = int(f.readline().strip())

        modPaths.append(LocalModInfo(rid, taint))
    return modPaths


class _CheckLocalModsUpdate:
    def __init__(
        self,
        finishCallback: Callable[[List[ModDownloadInfo]], None],
        errorCallback: Callable[[str], None],
    ) -> None:
        """参数参考 checkLocalModsUpdate()"""
        self.naManager = QNetworkAccessManager()
        self.finishCallback = finishCallback
        self.errorCallback = errorCallback
        self.receivedMods: List[ModData] = []
        self.errorOccurred = False
        self.receivedCount = 0

    def checkLocalModsUpdate(self):
        self.localModsInfo = getLocalMods()

        self.replies = modBatchRequest(
            self.naManager,
            [mod.rid for mod in self.localModsInfo],
            self.onFinished,
            self.onErrorOccurred,
        )

    def onFinished(self, replyIndex: int):
        if self.errorOccurred:
            return
        self.receivedCount += 1
        result = json.loads(bytes(self.replies[replyIndex].readAll().data()).decode())
        resultModList = [ModData(item) for item in result["data"]]
        self.receivedMods.extend(resultModList)
        # 如果该函数的调用计数次数等于replies数量，说明所有请求都已经完成，可以返回数据了。
        if self.receivedCount == len(self.replies):
            # 比较本地Mod和remote Mod，
            # remote Mod的getModFileLive("windows")返回值与本地Mod的taint不一样的就是需要更新的
            updateModRIDs: List[ModDownloadInfo] = []
            for remoteMod in self.receivedMods:
                rid = remoteMod.getResourceId()
                remoteFileLive = remoteMod.getModFileLive("windows")
                # 类似列表推导式的语法，把方括号换成圆括号表示这是一个生成器
                # 然后用next取出第一个值，避免一次性取出全部值
                localFileLive = next(
                    (modInfo for modInfo in self.localModsInfo if modInfo.rid == rid)
                ).taint
                if remoteFileLive != localFileLive:
                    updateModRIDs.append(
                        ModDownloadInfo(rid, remoteMod.getWindowsDownloadUrl())
                    )
            self.finishCallback(updateModRIDs)

    def onErrorOccurred(
        self, replyIndex: int, error: QtNetwork.QNetworkReply.NetworkError
    ):
        if self.errorOccurred:
            return
        self.errorOccurred = True
        self.errorCallback(error.name)


def checkLocalModsUpdate(
    finishCallback: Callable[[List[ModDownloadInfo]], None],
    errorCallback: Callable[[str], None],
):
    """检查本地Mod更新

    参数：
    finishCallback: 本地Mod更新检查完成时的回调，接收一个List[int]，代表需要更新的Mod的RID，该方法只会被调用一次，且如果错误发生，则不会被调用。
    errorCallback: 本地Mod更新检查出错时的回调，接收一个str，代表错误原因。该方法只会被调用一次。
    """

    obj = _CheckLocalModsUpdate(finishCallback, errorCallback)
    obj.checkLocalModsUpdate()


if __name__ == "__main__":
    app = QApplication()
    print(f"local mods count: {len(getLocalMods())}")

    def finishCallback(ls):
        print([i.rid for i in ls])
        print(f"need update count: {len(ls)}")

    def errorCallback(reason):
        print(f"error: {reason}")

    checkLocalModsUpdate(finishCallback, errorCallback)
    app.exec()
