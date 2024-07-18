import json
from typing import Callable, List, NamedTuple

from PySide6 import QtNetwork
from PySide6.QtNetwork import QNetworkAccessManager
from PySide6.QtWidgets import QApplication
from qfluentwidgets import QObject

import os

from common.mod.mod_data import ModData, modBatchRequest
from common.tricks import cached


INI_MOD_DIR_SUFFIX = "ModDirectory="
GAME_SETTING_PATH_BEHIND_HOME = r"AppData\Local\Pavlov\Saved\Config\Windows\GameUserSettings.ini"


class ModInstallationDirException(Exception):
    """Mod安装目录相关异常"""

    def __init__(self, details: str) -> None:
        super().__init__(details)


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
    resourceId: int
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
        with open(taintPath, "r", encoding="utf-8") as f:
            taint = int(f.readline().strip())

        modPaths.append(LocalModInfo(rid, taint))
    return modPaths


def checkIsInstalledAndLatest(modData: ModData):
    localMods = getLocalMods()
    # 在localMods中寻找id与modData一样的元组
    for localMod in localMods:
        if localMod.resourceId == modData.resourceId and localMod.taint == modData.getModFileLive(
            "windows"
        ):
            return True
    return False


class LocalModsUpdateChecker(QObject):
    """
    检查本地Mod更新

    参数：
    finishCallback: 本地Mod更新检查完成时的回调，接收一个List[int]，代表需要更新的Mod的RID，该方法只会被调用一次，且如果错误发生，则不会被调用。
    errorCallback: 本地Mod更新检查出错时的回调，接收一个str，代表错误原因。该方法只会被调用一次。
    """

    def __init__(
        self,
        finishCallback: Callable[[List[ModDownloadInfo]], None],
        errorCallback: Callable[[str], None],
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self.naManager = QNetworkAccessManager(self)
        self.finishCallback = finishCallback
        self.errorCallback = errorCallback
        self.receivedMods: List[ModData] = []
        self.errorOccurred = False
        self.receivedCount = 0
        self.localModsInfo = getLocalMods()

        self.replies = modBatchRequest(
            self.naManager,
            [mod.resourceId for mod in self.localModsInfo],
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
                rid = remoteMod.resourceId
                remoteFileLive = remoteMod.getModFileLive("windows")
                # 类似列表推导式的语法，把方括号换成圆括号表示这是一个生成器
                # 然后用next取出第一个值，避免一次性取出全部值
                localFileLive = next(
                    (modInfo for modInfo in self.localModsInfo if modInfo.resourceId == rid)
                ).taint
                if remoteFileLive != localFileLive:
                    updateModRIDs.append(ModDownloadInfo(rid, remoteMod.getWindowsDownloadUrl()))
            self.finishCallback(updateModRIDs)

    def onErrorOccurred(self, replyIndex: int, error: QtNetwork.QNetworkReply.NetworkError):
        if self.errorOccurred:
            return
        self.errorOccurred = True
        self.errorCallback(error.name)


def test1(app):
    print(f"local mods count: {len(getLocalMods())}")

    def finishCallback(ls):
        print([i.rid for i in ls])
        print(f"need update count: {len(ls)}")

    def errorCallback(reason):
        print(f"error: {reason}")

    LocalModsUpdateChecker(finishCallback, errorCallback, app)


if __name__ == "__main__":
    app = QApplication()
    test1(app)
    app.exec()
