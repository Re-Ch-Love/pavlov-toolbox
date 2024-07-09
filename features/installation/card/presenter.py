from typing import Any

from PySide6.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition
from features.common.global_objects import Globals
from features.common.mod_installation import ModInstallationJob, ModInstallationStage


class ModInstallationCardPresenter:
    def __init__(self, view: Any, job: ModInstallationJob) -> None:
        from features.installation.card.view import ModInstallationCardView

        self.view: ModInstallationCardView = view
        self.model: ModInstallationJob = job
        # self.finished: bool = False  # finished可能是成功完成，也可能是发生错误

    def updateDisplayData(self):
        self.model.update()
        match self.model.stage:
            # 下载阶段更新进度和下载速度
            case ModInstallationStage.downloading:
                self.view.updateProgress(
                    self.model.downloadInfo.completedLength,
                    self.model.downloadInfo.totalLength,
                )
                self.view.updateSpeed(self.model.downloadInfo.downloadSpeed)
            # 导入阶段只要切换UI即可，是一个无尽的进度条
            case ModInstallationStage.importing:
                self.view.disableCloseButton()
                self.view.switchToImportUi()
            # 成功或发生错误时，都标记自己已经完成。
            # 父级组件发现该card的presenter中finished==True时，应当从父级组件中删除该组件。
            # 父级组件检查finished==True时，应当调用getError方法查看是否有错误
            case ModInstallationStage.succeed:
                self.view.enableCloseButton()
                self.view.switchToSuccessUi()
                # 进入结束状态，第一次结束时，显示一个通知
                # if not self.finished:
                #     if not self.enableInfoBar:
                #         InfoBar.success(
                #             title=f"安装成功",
                #             content=self.model.cardName.displayName,
                #             position=InfoBarPosition.BOTTOM_RIGHT,
                #             orient=Qt.Orientation.Vertical,
                #             duration=3000,
                #             parent=self,
                #         )
                # self.finished = True
            case ModInstallationStage.error:
                self.view.enableCloseButton()
                self.view.switchToErrorUi(f"stage={self.model.stage.name},{self.getError()}")
                # 进入结束状态，第一次结束时，显示一个通知
                # if not self.finished:
                #     if not self.enableInfoBar:
                #         InfoBar.error(
                #             title=f"安装时发生错误",
                #             content=f"安装{self.model.cardName.displayName}时发生，原因为{self.getError()}",
                #             position=InfoBarPosition.BOTTOM_RIGHT,
                #             orient=Qt.Orientation.Vertical,
                #             duration=3000,
                #             parent=self,
                #         )
                # self.finished = True

    def getError(self) -> str:
        """获取错误，空字符串表示无错误"""
        return self.model.errorReason

    def getJob(self):
        return self.model
    
    def close(self):
        Globals.modInstallationManager.removeJob(self.model)
