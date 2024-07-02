import collections
from enum import Enum
from struct import unpack
from typing import Optional
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QSizePolicy, QWidget
from features.common import (
    byteLengthToHumanReadable,
    calculateProgresssPercentage,
    defaultIfNone,
)
from features.download_job import DownloadJob
from ui.download_card_ui import Ui_DownloadCard
from qfluentwidgets import FluentIcon, Theme, setTheme, toggleTheme


CardName = collections.namedtuple("CardName", "displayName hintName")

class DownloadCard(QWidget):
    paused = Signal()
    unpaused = Signal()
    closed = Signal()
    """点击close按钮时发送"""

    DISPLAY_NAME_FORMAT = '<span style=" font-size:16pt;">%s</span>'
    HINT_NAME_FORMAT = '<span style=" font-size:10pt; color:#737373;">（%s）</span>'

    def __init__(
        self,
        cardName: CardName = CardName("未知名称", ""),
        job: Optional[DownloadJob] = None
    ):
        super().__init__()
        self.job = defaultIfNone(job, DownloadJob())
        self.ui = Ui_DownloadCard()
        self.ui.setupUi(self)
        self.ui.progressBar.setValue(0)
        self.isDownloading = True
        self.ui.toggleButton.setIcon(FluentIcon.PAUSE)
        nameLabelText = self.DISPLAY_NAME_FORMAT % cardName.displayName
        if cardName.hintName:
            nameLabelText += self.HINT_NAME_FORMAT % cardName.hintName
        self.ui.nameLabel.setText(nameLabelText)

        self.ui.toggleButton.clicked.connect(self.toggle)
        self.ui.closeButton.setIcon(FluentIcon.CLOSE)
        self.ui.closeButton.clicked.connect(self.closed)
        # TODO close操作
        # self.ui.frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def toggle(self):
        if self.isDownloading:
            self.pause()
        else:
            self.unpause()

    def pause(self):
        if not self.isDownloading:
            return
        self.updateSpeed(0)
        self.ui.toggleButton.setIcon(FluentIcon.PLAY)
        self.isDownloading = False
        self.paused.emit()

    def unpause(self):
        if self.isDownloading:
            return
        self.ui.toggleButton.setIcon(FluentIcon.PAUSE)
        self.isDownloading = True
        self.unpaused.emit()

    def updateProgress(self, completedLength: int, totalLength: int):
        progressPercentage = calculateProgresssPercentage(
            completedLength, totalLength, 3
        )
        self.ui.progressBar.setValue(
            round(progressPercentage * self.ui.progressBar.maximum())
        )
        completedNum, completedUnit = byteLengthToHumanReadable(completedLength)
        totalNum, totalUnit = byteLengthToHumanReadable(totalLength)
        sizeText = f"{completedNum}{completedUnit} / {totalNum}{totalUnit}"
        # percentageText = str(round(progressPercentage * 100)) + "%"
        # labelText = f"{sizeText}  {percentageText}"
        self.ui.progressLabel.setText(sizeText)

    def updateSpeed(self, byteLengthPerSecond: int):
        num, unit = byteLengthToHumanReadable(byteLengthPerSecond)
        self.ui.speedLabel.setText(f"{num} {unit}/s")

    def updateByNewJob(self, newJob: DownloadJob):
        # 更新当前job并处理
        if self.job.status != newJob.status:
            match newJob.status:
                case "active":
                    self.unpause()
                case "waiting":
                    self.pause()
                case "paused":
                    self.pause()
                case "error":
                    self.pause()
                case "complete":
                    pass  # TODO
                case "removed":
                    pass  # TODO
        if self.job.totalLength != newJob.totalLength:
            pass  # 总字节数应该不会变，这里不处理
        if self.job.completedLength != newJob.completedLength:
            self.updateProgress(newJob.completedLength, newJob.totalLength)
        if self.job.downloadSpeed != newJob.downloadSpeed:
            self.updateSpeed(newJob.downloadSpeed)
        if self.job.errorCode != newJob.errorCode:
            pass  # TODO
        if self.job.errorMessage != newJob.errorMessage:
            pass  # TODO
        self.job = newJob


if __name__ == "__main__":
    # setTheme(Theme.DARK)
    app = QApplication()
    job = DownloadJob()
    window = DownloadCard(CardName("Dust 2 Mod", "Dust 2的依赖"))
    window.show()
    app.exec()
