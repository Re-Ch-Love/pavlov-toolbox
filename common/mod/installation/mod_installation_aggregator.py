from dataclasses import dataclass
from enum import Enum
from typing import List
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from common.log import AppLogger
from common.mod.installation.download_info import ModDownloadTaskInfo
from common.mod.installation.mod_download_manager import ModDownloadManager
from common.mod.installation.mod_import_dispatcher import (
    ModImportTaskDispatcher,
    ModImportTaskStatus,
)
from common.mod.mod_data import ModData


class ModInstallationStage(Enum):
    """安装阶段枚举类"""

    waiting = 1
    """等待中"""

    downloading = 2
    """下载中"""

    importing = 3
    """导入中"""

    succeed = 4
    """安装成功，只有导入成功了才会到这个阶段"""

    downloadError = 5
    """下载时发生错误"""

    importError = 6
    """导入时发生错误"""


@dataclass
class ModInstallationStatus:
    stage: ModInstallationStage
    downloadInfo: ModDownloadTaskInfo | None = None
    importTaskStatus: ModImportTaskStatus | None = None
    errorReason: str = ""


def _moveCompletedDownloadTaskToImportManager():
    """将下载管理器中的已完成任务移动到导入管理器"""
    downloadManager = ModDownloadManager.getInstance()
    importManager = ModImportTaskDispatcher.getInstance()
    for task in downloadManager.retrieveStopped():
        if task.status == "complete":
            importManager.addTask(task.gid, task.fileRelativePath, task.installationInfo)
            downloadManager.removeStoppedTask(task.gid)


def aggregateModInstallationStatus() -> List[ModInstallationStatus]:
    """从下载管理器和导入管理器中聚合安装信息"""
    _moveCompletedDownloadTaskToImportManager()
    downloadManager = ModDownloadManager.getInstance()
    importDispatcher = ModImportTaskDispatcher.getInstance()
    result: List[ModInstallationStatus] = []

    # 等待下载
    for task in downloadManager.retrieveWaiting():
        result.append(
            ModInstallationStatus(
                stage=ModInstallationStage.waiting,
                downloadInfo=task,
            )
        )

    # 下载中
    for task in downloadManager.retrieveActive():
        result.append(
            ModInstallationStatus(
                stage=ModInstallationStage.downloading,
                downloadInfo=task,
            )
        )

    # 下载失败
    for task in downloadManager.retrieveStopped():
        if task.status == "error":
            result.append(
                ModInstallationStatus(
                    stage=ModInstallationStage.downloadError,
                    downloadInfo=task,
                    errorReason=f"{task.errorMessage}(code={task.errorCode})",
                )
            )

    # 导入
    for status in importDispatcher.retrieveAllStatus():
        if status.finished and status.error is None:
            result.append(
                ModInstallationStatus(stage=ModInstallationStage.succeed, importTaskStatus=status)
            )
        elif status.finished and status.error is not None:
            result.append(
                ModInstallationStatus(
                    stage=ModInstallationStage.importError,
                    importTaskStatus=status,
                    errorReason=f"{status.error}",
                )
            )
        else:
            result.append(
                ModInstallationStatus(stage=ModInstallationStage.importing, importTaskStatus=status)
            )
    return result


def test1():
    app = QApplication()

    def poll():
        result = aggregateModInstallationStatus()
        AppLogger().debug(result)

    timer = QTimer()
    timer.setInterval(1000)
    timer.timeout.connect(poll)
    timer.start()
    # 3243988 有依赖的Mod
    # 3924157 大小小一些的Mod（zip大约80MB）
    ModDownloadManager.getInstance().addTask(
        ModData.constructFromApi(3924157), isCheckInstallationStatus=False
    )
    app.exec()


if __name__ == "__main__":
    test1()
