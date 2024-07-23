from enum import Enum
from typing import List, NamedTuple


import os

from common.log import AppLogger
from common.mod.installation.download_info import ModDownloadTaskInfo
from common.mod.installation.mod_import_dispatcher import ModImportTaskStatus
from common.mod.installation.path import getModInstallationDir
from common.mod.mod_data import ModData


class LocalModInfo(NamedTuple):
    """表示本地Mod信息的数据类，包括其资源ID和taint"""

    resourceId: int
    taint: int


def retrieveLocalMods() -> List[LocalModInfo]:
    """遍历Mod安装目录以获取本地Mod的信息

    Returns:
        List[LocalModInfo]: 存储所有本地Mod的LocalModInfo的列表
    """
    installationDir = getModInstallationDir()
    modPaths: List[LocalModInfo] = []
    for modDirName in os.listdir(installationDir):
        modDirFullPath = os.path.join(installationDir, modDirName)
        if not os.path.isdir(modDirFullPath):
            continue
        if not modDirName.startswith("UGC"):
            continue
        # 去除开头的UGC就是RID
        rid = int(modDirName[len("UGC") :])
        taintPath = os.path.join(modDirFullPath, "taint")
        with open(taintPath, "r", encoding="utf-8-sig") as f:
            taint = int(f.readline().strip())

        modPaths.append(LocalModInfo(rid, taint))
    return modPaths


class ModStatusInLocal(Enum):
    NOT_INSTALLED = 1
    OUTDATED = 2
    INSTALLED_AND_LATEST = 3
    INSTALLING = 4


def retrieveModsStatusInLocal(
    modDataList: List[ModData], localModsCache: List[LocalModInfo] | None = None
) -> List[ModStatusInLocal]:
    """

    不传入localModsCache时，每次调用将重新获取localMods（浪费性能，非必要情况尽可能缓存）"""
    from common.mod.installation.mod_installation_aggregator import aggregateModInstallationStatus

    if localModsCache is None:
        AppLogger().warning("在无缓存本地Mod数据的情况下检索Mod在本地的状态")
        localModsCache = retrieveLocalMods()

    modRidsMap: dict[int, ModData] = {modData.resourceId: modData for modData in modDataList}

    # 资源ID到本地状态的映射
    ridStatusMap = {}

    # 这里要先遍历本地Mod，再遍历安装中的Mod，否则如果有本地Mod正在安装，就会从INSTALLING变成OUTDATED

    # 遍历本地mod
    for localMod in localModsCache:
        if (rid := localMod.resourceId) not in modRidsMap:
            continue
        # 如果当前mod在localMods的rid中，且localMod的taint与mod的taint一致，为已安装
        if localMod.taint == modRidsMap[rid].taint:
            ridStatusMap[rid] = ModStatusInLocal.INSTALLED_AND_LATEST
        else:
            # 如果在rid中，但taint不一致，为需更新
            ridStatusMap[rid] = ModStatusInLocal.OUTDATED

    # 遍历当前所有安装中的Mod
    for status in aggregateModInstallationStatus():
        infoOrStatus: ModDownloadTaskInfo | ModImportTaskStatus
        if status.downloadInfo is not None:
            infoOrStatus = status.downloadInfo
        elif status.importTaskStatus is not None:
            infoOrStatus = status.importTaskStatus
        else:
            AppLogger().warning(
                "理论上不可达的代码：ModDownloadTaskInfo和ModImportTaskStatus都为空"
            )
            continue
        if (rid := infoOrStatus.installationInfo.modData.resourceId) in modRidsMap:
            ridStatusMap[rid] = ModStatusInLocal.INSTALLING

    # 整理前面得到的状态
    # 如果一个mod在ridStatusMap中没有对应的状态，说明本地没有安装，也不在安装中。即为NOT_INSTALLED
    return [
        (
            ridStatusMap[modData.resourceId]
            if modData.resourceId in ridStatusMap
            else ModStatusInLocal.NOT_INSTALLED
        )
        for modData in modDataList
    ]


def checkIsInstalledLatest(modData: ModData) -> bool:
    """检查给定的mod是否已安装最新版"""
    # Re-Ch:
    # 虽然每次调用这个函数时都会调用一次retrieveLocalMods()从Mod安装目录中遍历获取本地Mod数据
    # 不过经测试在我的电脑上这只花费大约0.015秒，所以还是可以接受的
    localMods = retrieveLocalMods()
    # 在localMods中寻找id与modData一样的元组
    for localMod in localMods:
        if localMod.resourceId == modData.resourceId and localMod.taint == modData.taint:
            return True
    return False


if __name__ == "__main__":
    pass
    # app = QApplication()
    # print([mod.resourceId for mod in getLocalMods()])
    # app.exec()
    # print(timeit.Timer(getLocalMods).timeit(number=1000))
