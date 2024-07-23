from logging import info
from turtle import down
from typing import List, cast
from PySide6.QtCore import QTimer

from common.mod.installation.download_info import ModDownloadTaskInfo
from common.mod.installation.mod_download_manager import ModDownloadManager
from common.mod.installation.mod_import_dispatcher import (
    ModImportTaskDispatcher,
    ModImportTaskStatus,
)
from common.mod.installation.mod_installation_aggregator import (
    ModInstallationStatus,
    ModInstallationStage,
    aggregateModInstallationStatus,
)
from common.utils import byteLengthToHumanReadable
from ui.installation.card import colors
from ui.installation.card.options import ModInstallationCardOptions
from ui.installation.card.view import ModInstallationCardView


def formatMirrorStationsPrompt(dlInfo: ModDownloadTaskInfo) -> str:
    prompt: str
    if dlInfo.installationInfo.mirrorStationNames:
        mirrorsStationsText = "、".join(dlInfo.installationInfo.mirrorStationNames)
        prompt = f"通过{mirrorsStationsText}加速下载"
    else:
        prompt = ""
    return prompt


def formatProgressInfo(dlInfo: ModDownloadTaskInfo):
    completedNum, completedUnit = byteLengthToHumanReadable(dlInfo.completedLength)
    totalNum, totalUnit = byteLengthToHumanReadable(dlInfo.totalLength)
    speedNum, speedUnit = byteLengthToHumanReadable(dlInfo.downloadSpeed)
    return f"{completedNum}{completedUnit} / {totalNum}{totalUnit}  {speedNum} {speedUnit}/s"


def convertInstallationInfoToCardOptions(
    status: ModInstallationStatus,
) -> ModInstallationCardOptions:
    match status.stage:
        case ModInstallationStage.waiting:
            dlInfo = cast(ModDownloadTaskInfo, status.downloadInfo)
            return ModInstallationCardOptions(
                progressBarPercentage=0,
                progressBarColor=None,
                progressInfo="等待下载",
                prompt=formatMirrorStationsPrompt(dlInfo),
                closeButtonClickedCallback=lambda: ModDownloadManager.getInstance().stopAndRemoveTask(
                    dlInfo.gid
                ),
                modName=dlInfo.installationInfo.modName,
            )
        case ModInstallationStage.downloading:
            dlInfo = cast(ModDownloadTaskInfo, status.downloadInfo)
            return ModInstallationCardOptions(
                progressBarPercentage=calculateProgressPercentage(
                    dlInfo.completedLength, dlInfo.totalLength, 3
                ),
                progressBarColor=None,
                progressInfo=formatProgressInfo(dlInfo),
                prompt=formatMirrorStationsPrompt(dlInfo),
                closeButtonClickedCallback=lambda: ModDownloadManager.getInstance().stopAndRemoveTask(
                    dlInfo.gid
                ),
                modName=dlInfo.installationInfo.modName,
            )
        case ModInstallationStage.importing:
            importStatus = cast(ModImportTaskStatus, status.importTaskStatus)
            return ModInstallationCardOptions(
                progressBarPercentage=-1,
                progressBarColor=None,
                closeButtonClickedCallback=None,
                modName=importStatus.installationInfo.modName,
                prompt="",
                progressInfo="解压并导入中...",
            )
        case ModInstallationStage.succeed:
            importStatus = cast(ModImportTaskStatus, status.importTaskStatus)
            return ModInstallationCardOptions(
                progressBarPercentage=1,
                progressBarColor=colors.SUCCESS_COLOR,
                modName=importStatus.installationInfo.modName,
                closeButtonClickedCallback=lambda: ModImportTaskDispatcher.getInstance().removeFinishedTask(
                    importStatus.gid
                ),
                prompt="",
                progressInfo="导入成功",
            )
        case ModInstallationStage.downloadError:
            dlInfo = cast(ModDownloadTaskInfo, status.downloadInfo)
            return ModInstallationCardOptions(
                progressBarPercentage=1,
                progressBarColor=colors.ERROR_COLOR,
                modName=dlInfo.installationInfo.modName,
                closeButtonClickedCallback=lambda: ModDownloadManager.getInstance().stopAndRemoveTask(
                    dlInfo.gid
                ),
                prompt="",
                progressInfo=f"下载时发生错误：{status.errorReason}",
            )
        case ModInstallationStage.importError:
            importStatus = cast(ModImportTaskStatus, status.importTaskStatus)
            return ModInstallationCardOptions(
                progressBarPercentage=1,
                progressBarColor=colors.ERROR_COLOR,
                modName=importStatus.installationInfo.modName,
                closeButtonClickedCallback=lambda: ModImportTaskDispatcher.getInstance().removeFinishedTask(
                    importStatus.gid
                ),
                prompt="",
                progressInfo=f"导入时发生错误：{status.errorReason}",
            )
        case _:
            raise RuntimeError("Unreachable code")


def calculateProgressPercentage(completedLength: int, totalLength: int, n: int) -> float:
    """返回下载进度百分比，保留`n`位小数，取值范围[0, 1]，如果`totalLength`为0则返回0.0"""
    if totalLength != 0:
        percentage = round(completedLength / totalLength, n)
    else:
        percentage = 0.0
    return percentage


# 按照下载、导入、等待、成功、失败的顺序排序
CARD_ORDER = [
    ModInstallationStage.downloading,
    ModInstallationStage.importing,
    ModInstallationStage.waiting,
    ModInstallationStage.succeed,
    ModInstallationStage.downloadError,
    ModInstallationStage.importError,
]


class ModInstallationPresenter:
    def __init__(self, view) -> None:
        from ui.installation.view import ModInstallationManagerView

        self.view: ModInstallationManagerView = view

        self.isShow = False
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.pollingUpdate)
        self.timer.start()

    def pollingUpdate(self):
        statusList = aggregateModInstallationStatus()
        if self.isShow:
            # 为status排序
            statusList.sort(key=lambda status: CARD_ORDER.index(status.stage))
            optsList = [convertInstallationInfoToCardOptions(status) for status in statusList]
            self.view.renderCards(optsList)
