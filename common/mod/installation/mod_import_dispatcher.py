import hashlib
import os
import random
import shutil
import time
from typing import Dict, List, NamedTuple
from uuid import uuid4
import zipfile

from PySide6.QtCore import QRunnable, QThreadPool
import requests
import app_config
from common.log import AppLogger
from common.mod.installation.extra_info import ModInstallationInfo
from common.mod.installation.mod_name import ModName
from common.mod.installation.path import getModInstallationDir
from common.mod.mod_data import ModData


class ModImportTaskStatus(NamedTuple):
    gid: str
    installationInfo: ModInstallationInfo
    finished: bool
    error: Exception | None


class ModImportTaskDispatcher:
    """Mod导入任务调度器

    单例对象，使用ModInstallationManager.getInstance()获取


    - 向调度器添加任务，调度器会自动执行任务，且不阻塞主线程。
    - 添加任务时，返回一个gid，用于关闭任务
    - 使用tellAllStatus方法可以获取所有任务的执行状态
    - 正在执行的任务不可中断
    - 使用close方法可以关闭已经完成的任务
    """

    _instance: "ModImportTaskDispatcher | None" = None

    @classmethod
    def getInstance(cls) -> "ModImportTaskDispatcher":
        if cls._instance is None:
            cls._instance = ModImportTaskDispatcher()
        return cls._instance

    def __new__(cls) -> "ModImportTaskDispatcher":
        if ModImportTaskDispatcher._instance:
            AppLogger().warning(
                "尝试直接构造ModImportTaskDispatcher对象，请使用ModImportTaskDispatcher.getInstance()"
            )
            return ModImportTaskDispatcher._instance
        ModImportTaskDispatcher._instance = super().__new__(cls)
        return ModImportTaskDispatcher._instance

    def __init__(self) -> None:
        self.tasks: Dict[str, ModImportWorker] = {}
        self.threadpool = QThreadPool.globalInstance()

    def addTask(self, gid: str, zipFilePath: str, info: ModInstallationInfo):
        # AppLogger().debug(f"正在为{modData}启动导入线程")
        worker = ModImportWorker(zipFilePath, info)
        print(id(worker))
        self.threadpool.start(worker)
        self.tasks[gid] = worker

    def addMockTask(self, n: int = 1):
        for _ in range(n):
            gid = uuid4().hex
            worker = MockModImportWorker()
            # 运行后不要自动删除对象
            # worker.setAutoDelete(False)
            self.threadpool.start(worker)
            self.tasks[gid] = worker

    def retrieveAllStatus(self) -> List[ModImportTaskStatus]:
        # AppLogger().debug(self.tasks)
        return [
            ModImportTaskStatus(gid, worker.info, worker.finished, worker.error)
            for gid, worker in self.tasks.items()
        ]

    def removeFinishedTask(self, gid: str):
        if gid not in self.tasks:
            AppLogger().warning(f"要移除的导入任务不存在（gid={gid}）")
            return
        if not self.tasks[gid].finished:
            AppLogger().warning(f"要移除的导入任务未结束（gid={gid}）")
            return
        del self.tasks[gid]


class ModImportWorker(QRunnable):
    def __init__(self, zipFilePath: str, info: ModInstallationInfo):
        super().__init__()
        self.zipFilePath: str = zipFilePath
        self.info: ModInstallationInfo = info
        self.finished: bool = False
        self.error: Exception | None = None

    def run(self):
        try:
            AppLogger().info(f"开始导入{self.info.modData}")
            _importMod(self.zipFilePath, self.info.modData)
        except Exception as e:
            AppLogger().info(f"导入{self.info.modData}时发生错误：{e}")
            self.error = e
        finally:
            AppLogger().info(f"导入{self.info.modData}结束")
            self.finished = True


def _importMod(zipFilePath: str, modData: ModData):
    """导入Mod

    分为哈希校验，解压、补全、移动文件夹四个步骤"""
    _md5Check(zipFilePath, modData)
    # 定义该Mod解压补全时的临时目录路径
    tempDir = os.path.join(app_config.TEMP_IMPORT_MOD_DIR, f"UGC{modData.resourceId}")
    _unzipModData(tempDir, zipFilePath)
    _writeTaintFile(tempDir, str(modData.taint))
    _moveModTempDirToInstallationDir(tempDir)
    # 安装完成后删除原始文件
    os.remove(zipFilePath)


class Md5MismatchException(Exception):
    def __str__(self) -> str:
        return "MD5不匹配"


MD5_URL = "https://api.pavlov-toolbox.rech.asia/modio/v1/games/3959/mods/%d/files/%d/"


def _md5Check(filePath: str, modData: ModData):
    response = requests.get(MD5_URL % (modData.resourceId, modData.taint))
    response.raise_for_status()
    resultObj = response.json()
    targetMd5 = resultObj["filehash"]["md5"]
    with open(filePath, "rb") as f:
        bytes = f.read()  # read file as bytes
        localMd5 = hashlib.md5(bytes).hexdigest()
    if localMd5 != targetMd5:
        raise Md5MismatchException()


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


class MockModImportWorker(ModImportWorker):
    def __init__(self):
        super().__init__("", ModInstallationInfo(ModData({}), ModName("", ""), [""]))

    def run(self):
        # 随机休眠[2, 5]秒模拟耗时
        time.sleep(random.uniform(2, 5))
        # 一半概率有错误
        if random.choice([True, False]):
            self.error = Exception("模拟错误")
        self.finished = True


if __name__ == "__main__":
    # modImportDispatcher = ModImportTaskDispatcher.getInstance()
    # modImportDispatcher.addMockTask(3)
    # print(modImportDispatcher.retrieveAllStatus())
    # time.sleep(4)
    # print(modImportDispatcher.retrieveAllStatus())
    mod = ModData.constructFromApi(2803451)
    _md5Check(
        r"C:\Users\kongc\AppData\Local\Temp\PavlovToolboxTemp\downloads\modfile_2803451.87.zip", mod
    )
