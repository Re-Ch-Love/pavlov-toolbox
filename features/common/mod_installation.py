from enum import Enum
import os
import os
import random
import time
from uuid import uuid4
import zipfile
import shutil

from PySide6.QtNetwork import QNetworkReply
import app_config
from typing import Dict, List, NamedTuple, Optional, Self

from PySide6.QtCore import QRunnable, QThreadPool
from qfluentwidgets import QObject
from aria2.aria2 import Aria2
from features.common.global_objects import Globals
from features.common.local_mods import checkIsInstalledAndLatest, getModInstallationDir
from features.common.mod_mirrors import getDownloadUrlFromFrostBladeMirror
from features.common.mod_dependencies import ModDependenciesProcessor
from features.common.tricks import Fn
from features.common.download_info import DownloadInfo
from features.common.mod import ModData
from PySide6.QtCore import Signal


def importMod(zipFilePath: str, modData: ModData):
    """导入Mod

    分为解压、补全、移动文件夹三个步骤"""
    # 定义该Mod解压补全时的临时目录路径
    tempDir = os.path.join(
        app_config.IMPORT_MOD_TEMP_DIR, f"UGC{modData.getResourceId()}"
    )
    _unzipModData(tempDir, zipFilePath)
    _writeTaintFile(tempDir, str(modData.getModFileLive("windows")))
    _moveModTempDirToInstallationDir(tempDir)
    # 安装完成后删除原始文件
    os.remove(zipFilePath)


def _unzipModData(outputDir: str, zipFilePath: str):
    # 如果输出目录存在，则清空
    if os.path.exists(outputDir):
        shutil.rmtree(outputDir)
    else:
        os.makedirs(outputDir)
    outputDir = os.path.join(outputDir, "Data")
    # 使用zipfile模块解压ZIP文件到目标目录
    with zipfile.ZipFile(zipFilePath, "r") as zip_file:
        zip_file.extractall(outputDir)


def _writeTaintFile(outputDir: str, content: str):
    taintFilePath = os.path.join(outputDir, "taint")
    with open(taintFilePath, "w", encoding="utf-8") as file:
        file.write(content)


def _moveModTempDirToInstallationDir(sourceDir: str):
    r"""将Mod从临时目录移动到安装目录"""
    modInstallationDir = getModInstallationDir()
    # 判断安装目录是否存在，如果不存在则新建
    if not os.path.exists(modInstallationDir):
        os.makedirs(modInstallationDir)
    # 获取源目录最后一段（即目录名称）
    modDirName = os.path.basename(sourceDir)
    targetDir = os.path.join(modInstallationDir, modDirName)
    # 如果目录存在，使用shutil递归删除目录
    if os.path.exists(targetDir):
        shutil.rmtree(targetDir)
    # 使用shutil移动目录
    shutil.move(sourceDir, targetDir)


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


class ModImportWorkerSignals(QObject):
    completed = Signal()
    errorOccurred = Signal(str)


class ModImportWorker(QRunnable):
    def __init__(self, zipFilePath: str, modData: ModData):
        super().__init__()
        self.zipFilePath = zipFilePath
        self.modData = modData
        self.signals = ModImportWorkerSignals()

    def run(self):
        try:
            importMod(self.zipFilePath, self.modData)
        except Exception as e:
            self.signals.errorOccurred.emit(str(e))
        else:
            self.signals.completed.emit()


# Re-Ch: 我认为这个类写的非常的烂，后面有时间我会改掉它
class ModInstallationJob:
    """
    表示Mod安装工作的类

    只需要不停的调用（例如间隔1s）其update()方法，即可刷新阶段信息。
    在调用update前，即使前一个阶段的工作已经完成，也不会进入下一个阶段。（只有调用update()时才会检测当前阶段是否完成）

    stage为error时，errorReason字段表示错误原因
    """

    def __init__(self, gid: str, cardName: CardName, modData: ModData) -> None:
        """
        参数 `urls`：内容为相同资源的url列表（可以只传入一个）
        """
        self.gid = gid
        self.modData = modData
        self.cardName = cardName
        self.stage = ModInstallationStage.downloading
        self.downloadInfo = DownloadInfo()
        self.errorReason: str = ""

    def update(self):
        match self.stage:
            case ModInstallationStage.downloading:
                self._updateDownloadInfo()
                # TODO 补全其它状态信息
                if self.downloadInfo.status == "complete":
                    self._enterImportStatus()
                    self.stage = ModInstallationStage.importing
            case ModInstallationStage.importing:
                pass  # 不必处理，有槽函数修改
            case ModInstallationStage.succeed:
                pass  # 不做处理
            case ModInstallationStage.error:
                pass  # 不做处理

    def _updateDownloadInfo(self):
        raw = aria2.tellStatus(self.gid, DownloadInfo.ARIA2_RPC_KEYS)
        info = DownloadInfo()
        info.loadFromAria2RawData(raw["result"])
        self.downloadInfo = info
        if info.errorCode:
            self.stage = ModInstallationStage.error
            self.errorReason = f"code: {info.errorCode}, msg: {info.errorMessage}"

    def _enterImportStatus(self):
        """进入导入阶段的一些准备工作"""
        # 创建并启动导入的线程
        threadpool = QThreadPool.globalInstance()
        self.worker = ModImportWorker(self.downloadInfo.fileRelativePath, self.modData)
        self.worker.signals.completed.connect(self._onImportCompleted)
        self.worker.signals.errorOccurred.connect(self._onImportErrorOccurred)
        threadpool.start(self.worker)

    def _onImportCompleted(self):
        self.stage = ModInstallationStage.succeed
        self.isImportComplete = True

    def _onImportErrorOccurred(self, error: str):
        self.stage = ModInstallationStage.error
        self.importError = error


class MockModInstallationJob(ModInstallationJob):
    """
    模拟ModInstallationJob，用于测试界面
    """

    def __init__(
        self,
        downloadTime: Optional[int] = None,
        importTime: Optional[int] = None,
        willOccurError: Optional[bool] = None,
    ) -> None:
        self.gid = str(uuid4())
        self.stage = ModInstallationStage.downloading
        self.cardName = CardName(f"模拟数据{self.gid[:6]}", self.gid)
        self.downloadInfo = DownloadInfo()
        self.modInstallationDirPath = ""
        self.errorReason: str = ""

        # 随机3s-10s后下载完成
        self.endDownloadingTime = (
            time.time() + random.randint(3, 10)
            if downloadTime is None
            else downloadTime
        )
        # 下载完成后，随机1s-5s后导入完成
        self.endImportingTime = (
            self.endDownloadingTime + random.randint(1, 5)
            if importTime is None
            else importTime
        )
        # 显示错误还是成功
        self.willOccurError = (
            random.choice([True, False]) if willOccurError is None else willOccurError
        )

    def update(self):
        match self.stage:
            case ModInstallationStage.downloading:
                if time.time() > self.endDownloadingTime:
                    # print(f"{self.gid[:6]} enter importing stage")
                    self.stage = ModInstallationStage.importing
            case ModInstallationStage.importing:
                if time.time() > self.endImportingTime:
                    # print(f"{self.gid[:6]} enter succeed stage")
                    if self.willOccurError:
                        self.stage = ModInstallationStage.error
                        self.errorReason = "测试错误"
                    else:
                        self.stage = ModInstallationStage.succeed

            case ModInstallationStage.succeed:
                pass  # 不做处理
            case ModInstallationStage.error:
                pass  # 不做处理


class ModInstallationManager:
    """Mod安装管理器
    
    单例对象
    """
    
    @staticmethod
    def getInstance() -> Self:
        if not hasattr(ModInstallationManager, "_instance"):
            ModInstallationManager._instance = ModInstallationManager()
        return ModInstallationManager._instance
    
    def __init__(self) -> None:
        self._jobs: List[ModInstallationJob] = []
        self.dependencyProcessors: Dict[int, ModDependenciesProcessor] = {}

    def addJob(self, modData: ModData, cardName: CardName | None = None) -> None:
        if cardName is None:
            cardName = CardName(modData.getName(), "")
        if checkIsInstalledAndLatest(modData):
            return
        downloadUrls = [modData.getWindowsDownloadUrl()]
        def download():
            if app_config.DEBUG:
                print(f"下载地址：{downloadUrls}")
            gid = aria2.addUri(downloadUrls)
            job = ModInstallationJob(gid, cardName, modData)
            self._jobs.append(job)
            # 检查依赖项
            self.addJobDependencies(modData)
            
        # 尝试获取镜像站链接
        def afterGetMirrorUrl(mirrorUrl: str) -> None:
            if mirrorUrl:
                downloadUrls.append(mirrorUrl)
            download()
            
        def whenGetMirrorUrlError(error: QNetworkReply.NetworkError):
            print(f"get FrostBlade mirror error: {error.name}")
            download()

        (getDownloadUrlFromFrostBladeMirror(Globals.qRequestReady, modData.getResourceId())
            .then(afterGetMirrorUrl)
            .catch(whenGetMirrorUrlError))

    def addJobDependencies(self, modData: ModData):
        obj = ModDependenciesProcessor(
            modData,
            self._getModDependenciesFinish,
            self._getModDependenciesError,
        )
        # 因为ModDependenciesProcessor是一个QObject，如果不提供parent，它会被回收掉。
        # 而ModInstallationManger在应用中是一个全局单例，所以只要把ModDependenciesProcessor的实例保存在属性的字典中
        # 就不会被回收了，但是用完了要用del self.dependencyProcessors[modData.getResourceId()]来释放，不然会内存溢出
        self.dependencyProcessors[modData.getResourceId()] = obj

    def _getModDependenciesFinish(self, modData: ModData, dependencies: List[ModData]):
        for dependency in dependencies:
            self.addJob(
                dependency,
                CardName(dependency.getName(), f"{modData.getName()} 的依赖"),
            )
        del self.dependencyProcessors[modData.getResourceId()]

    def _getModDependenciesError(self, modData: ModData, error: str):
        # 暂时没必要对错误作处理
        print(f"{modData.getName()} 的依赖获取失败：{error}")
        del self.dependencyProcessors[modData.getResourceId()]

    def addMockJob(self, count: int):
        Fn(lambda: self._jobs.append(MockModInstallationJob())).repeat(count)

    def updateAllJobs(self):
        for job in self._jobs:
            job.update()
            # if job.stage == ModInstallationStage.succeed:
            # self._jobs.remove(job)

    def getAllJobs(self):
        self.updateAllJobs()
        return self._jobs

    def showJobs(self):
        print("\n".join([f"{job.cardName} in {job.stage}" for job in self._jobs]))

    def removeJob(self, job: ModInstallationJob):
        self._jobs.remove(job)
        if job.stage == ModInstallationStage.downloading:
            aria2.remove(job.gid)


# def test2():
#     # 这是一个有依赖的Mod
#     manager = ModInstallationManager()
#     mod = ModData.constructFromServer(3243988)
#     manager.addJob(mod, CardName(mod.getName(), ""))
#     QTimer.singleShot(3000, lambda: manager.showJobs())


if __name__ == "__main__":
    # importMod(".\\downloads\\modfile_2802847.129.zip", ModData.constructFromServer(2802847))
    app = Globals.createQApp()
    # test2()
    # app.exec()

