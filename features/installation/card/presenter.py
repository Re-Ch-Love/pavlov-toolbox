from typing import Any
from features.common.mod_installation import ModInstallationJob, ModInstallationStage


class ModInstallationCardPresenter:
    def __init__(self, view: Any, job: ModInstallationJob) -> None:
        from features.installation.card.view import ModInstallationCardView

        self.view: ModInstallationCardView = view
        self.model: ModInstallationJob = job
        self.finished: bool = False
        """finished可能是成功完成，也可能是发生错误"""

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
                self.view.switchToImportUi()
            # 成功或发生错误时，都标记自己已经完成。
            # 父级组件发现该card的presenter中finished==True时，应当从父级组件中删除该组件。
            # 父级组件检查finished==True时，应当调用getError方法查看是否有错误
            case ModInstallationStage.succeed | ModInstallationStage.error:
                self.finished = True

    def getError(self) -> str:
        """获取错误，空字符串表示无错误"""
        return self.model.errorReason
    
    def getJob(self):
        return self.model
