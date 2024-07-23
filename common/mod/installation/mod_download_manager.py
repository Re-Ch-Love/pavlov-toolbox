from PySide6.QtCore import QTimer
from PySide6.QtNetwork import QNetworkReply
from PySide6.QtWidgets import QApplication
from typing import Dict, List

from qfluentwidgets import QObject
from aria2.aria2_client import Aria2Client

from common.log import AppLogger
from common.mod.installation.extra_info import ModInstallationInfo
from common.mod.installation.download_info import ModDownloadTaskInfo
from common.mod.installation.mod_dependencies import getModDependencies
from common.mod.installation.mod_name import (
    ModName,
)
from common.mod.local_mods import (
    checkIsInstalledLatest,
)
from common.mod.mod_mirrors import getDownloadUrlFromFrostBladeMirror
from common.mod.mod_data import ModData


class ModDownloadManager(QObject):
    """Mod下载管理器

    单例对象，使用ModInstallationManager.getInstance()获取
    """

    _instance: "ModDownloadManager | None" = None

    @classmethod
    def getInstance(cls) -> "ModDownloadManager":
        if cls._instance is None:
            cls._instance = ModDownloadManager()
        return cls._instance

    def __new__(cls) -> "ModDownloadManager":
        if ModDownloadManager._instance:
            AppLogger().warning(
                "尝试直接构造ModDownloadManager对象，请使用ModDownloadManager.getInstance()"
            )
            return ModDownloadManager._instance
        ModDownloadManager._instance = super().__new__(cls)
        return ModDownloadManager._instance

    def __init__(self) -> None:
        super().__init__()
        self.aria2c = Aria2Client()
        self.gidToInfo: Dict[str, ModInstallationInfo] = {}

    def addTask(
        self,
        modData: ModData,
        modName: ModName | None = None,
        isCheckInstallationStatus: bool = False,
    ) -> None:
        """添加安装任务

        Args:
            modData (ModData): 要安装的Mod的ModData
            modName (ModName | None, optional): Mod名称. Defaults to None.
            isCheckInstallationStatus (bool, optional): 是否启用安装状态检查，即如果本地已经安装且是最新，则跳过. Defaults to False.
        """
        if modName is None:
            modName = ModName(modData.name, "")
        # 如果启用安装状态检查 and 已经安装最新版，则不添加该Mod的安装任务
        if isCheckInstallationStatus and checkIsInstalledLatest(modData):
            AppLogger().info(f"{modName}已经安装最新版，跳过")
            # 处理该Mod的依赖，处理时还会调用addJob方法，所以依赖如果不是最新就会被安装
            self.processModDependencies(modData, isCheckInstallationStatus)
            return
        # 下载地址列表
        downloadUrls: List[str] = []
        # 镜像站名称，如果有镜像站，会在安装卡片中显示
        mirrorStationNames: List[str] = []

        # 定义添加下载任务函数
        def addDownloadTask():
            # 如果该Mod已经在下载列表中，则不添加，防止在处理依赖时，多个Mod依赖同一个Mod，导致该Mod下载多次
            ridGidMap = {info.modData.resourceId: gid for gid, info in self.gidToInfo.items()}
            if modData.resourceId in ridGidMap:
                # 合并一下两个ModName
                info = self.gidToInfo[ridGidMap[modData.resourceId]]
                oldModName = info.modName
                info.modName = ModName(
                    oldModName.mainName,
                    (
                        f"{oldModName.hintName} | {modName.hintName}"
                        if oldModName.hintName
                        else modName.hintName
                    ),
                )
                AppLogger().info(f"{modName}已经在下载列表中，跳过")
                return
            # 把官方的下载地址放在最后，这样镜像站的优先级更高
            downloadUrls.append(modData.getWindowsDownloadUrl())
            gid = self.aria2c.addUri(downloadUrls)
            AppLogger().info(f"添加下载任务：{{modName={modName}, gid={gid}, url={downloadUrls}}}")
            # 添加到extra中
            self.gidToInfo[gid] = ModInstallationInfo(modData, modName, mirrorStationNames)
            # 处理依赖
            self.processModDependencies(modData, isCheckInstallationStatus)

        # 定义获取镜像站下载链接后的处理函数
        def afterGetMirrorUrl(mirrorUrl: str) -> None:
            if mirrorUrl:
                downloadUrls.append(mirrorUrl)
                mirrorStationNames.append("FrostBlade镜像站")
            addDownloadTask()

        # 定义获取下载站链接出错时的处理函数
        def whenGetMirrorUrlError(error: QNetworkReply.NetworkError):
            AppLogger().warning(f"get FrostBlade mirror error: {error.name}")
            addDownloadTask()

        (
            # 先从镜像站获取该Mod的下载链接
            getDownloadUrlFromFrostBladeMirror(self, modData.resourceId)
            # 如果有镜像链接，则加入下载url列表中并开始下载；如果没有则直接开始下载
            .then(afterGetMirrorUrl)
            # 如果获取镜像链接时发生错误，直接开始下载
            .catch(whenGetMirrorUrlError).done()
        )

    def processModDependencies(self, modData: ModData, isCheckLocalStatus: bool):
        """处理Mod依赖，如果有依赖则会使用addJob添加下载

        Args:
            modData (ModData): 要处理依赖的ModData
            isCheckLocalStatus (bool): 这个参数将在有依赖Mod时传入给addJob，因此请参考`addJob`
        """
        (
            getModDependencies(self, modData.resourceId)
            .then(
                lambda modDataList: [
                    self.addTask(
                        dependencyModData,
                        ModName(dependencyModData.name, f"{modData.name} 的依赖"),
                        isCheckLocalStatus,
                    )
                    for dependencyModData in modDataList
                ]
            )
            .done()
        )

    def retrieveActive(self) -> List[ModDownloadTaskInfo]:
        response = self.aria2c.tellActive()
        result = response["result"]
        return [ModDownloadTaskInfo(raw, self.gidToInfo[raw["gid"]]) for raw in result]

    def retrieveWaiting(self) -> List[ModDownloadTaskInfo]:
        response = self.aria2c.tellWaiting(0, 200)
        result = response["result"]
        return [ModDownloadTaskInfo(raw, self.gidToInfo[raw["gid"]]) for raw in result]

    def stopAndRemoveTask(self, gid: str):
        self.aria2c.remove(gid)
        self.removeStoppedTask(gid)

    def retrieveStopped(self) -> List[ModDownloadTaskInfo]:
        response = self.aria2c.tellStopped(0, 200)
        result = response["result"]
        return [ModDownloadTaskInfo(raw, self.gidToInfo[raw["gid"]]) for raw in result]

    def removeStoppedTask(self, gid: str):
        self.gidToInfo.pop(gid, None)  # 要指定一个默认值，否则键不存在时会抛出异常
        self.aria2c.removeDownloadResult(gid)


def test1():
    app = QApplication()
    # 这是一个有依赖的Mod
    manager = ModDownloadManager.getInstance()
    mod = ModData.constructFromApi(3243988)
    manager.addTask(mod, ModName(mod.name, ""), isCheckInstallationStatus=False)
    QTimer.singleShot(8_000, lambda: print(len(manager.retrieveActive())))
    app.exec()


def test2():
    app = QApplication()
    ModDownloadManager.getInstance().addTask(
        ModData.constructFromApi(3243988), isCheckInstallationStatus=False
    )

    def poll():
        infoList = ModDownloadManager.getInstance().retrieveActive()
        AppLogger().debug(
            "aria2.tellActive"
            + str([(info.installationInfo.modName, info.status) for info in infoList])
        )
        infoList = ModDownloadManager.getInstance().retrieveWaiting()
        AppLogger().debug(
            "aria2.tellWaiting"
            + str([(info.installationInfo.modName, info.status) for info in infoList])
        )
        infoList = ModDownloadManager.getInstance().retrieveStopped()
        AppLogger().debug(
            "aria2.tellStopped"
            + str([(info.installationInfo.modName, info.status) for info in infoList])
        )

    timer = QTimer()
    timer.setInterval(1000)
    timer.timeout.connect(poll)
    timer.start()
    app.exec()


def test3():
    """多次添加同一个url"""
    app = QApplication()
    mod = ModData.constructFromApi(3924157)
    ModDownloadManager.getInstance().addTask(mod)
    ModDownloadManager.getInstance().addTask(mod)
    ModDownloadManager.getInstance().addTask(mod)

    def poll():
        infoList = ModDownloadManager.getInstance().retrieveActive()
        AppLogger().debug(f"len(aria2.tellActive) == {len(infoList)}")

    timer = QTimer()
    timer.setInterval(1000)
    timer.timeout.connect(poll)
    timer.start()
    app.exec()


if __name__ == "__main__":
    test3()
