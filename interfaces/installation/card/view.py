from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QColor

from qfluentwidgets import FluentIcon, IndeterminateProgressBar, ProgressBar

import app_config
from common.mod.mod_installation import MockModInstallationJob, ModInstallationJob
from common.tricks import onceMethod
from interfaces.installation.card.presenter import ModInstallationCardPresenter
from ui_design.installation_card_ui import Ui_InstallationCard

class ModInstallationCardView(QWidget, Ui_InstallationCard):
    # closed = Signal()
    # """点击close按钮时发送"""

    DISPLAY_NAME_FORMAT = '<span style=" font-size:16pt;">%s</span>'
    HINT_NAME_FORMAT = '<span style=" font-size:10pt; color:#737373;">（%s）</span>'

    def __init__(
        self,
        job: ModInstallationJob,
    ):
        super().__init__()
        self.presenter = ModInstallationCardPresenter(self, job)
        self.setupUi(self)
        self.progressBar.setValue(0)
        nameLabelText = self.DISPLAY_NAME_FORMAT % job.cardName.displayName
        if job.cardName.hintName:
            nameLabelText += self.HINT_NAME_FORMAT % job.cardName.hintName
        self.nameLabel.setText(nameLabelText)

        self.closeButton.setIcon(FluentIcon.CLOSE)
        # self.closeButton.clicked.connect(self.closed)
        self.closeButton.clicked.connect(self.presenter.close)
        # self.isImportUi = False
        if job.mirrorStationNames:
            mirrorsStationsText = "、".join(job.mirrorStationNames)
            self.mirrorStationsLabel.setText(f"通过{mirrorsStationsText}加速下载")
        else:
            self.mirrorStationsLabel.setText("")

    def disableCloseButton(self):
        self.closeButton.setEnabled(False)
    
    def enableCloseButton(self):
        self.closeButton.setEnabled(True)

    def updateProgress(self, completedLength: int, totalLength: int):
        progressPercentage = calculateProgressPercentage(
            completedLength, totalLength, 3
        )
        self.progressBar.setValue(
            round(progressPercentage * self.progressBar.maximum())
        )
        completedNum, completedUnit = byteLengthToHumanReadable(completedLength)
        totalNum, totalUnit = byteLengthToHumanReadable(totalLength)
        sizeText = f"{completedNum}{completedUnit} / {totalNum}{totalUnit}"
        self.progressLabel.setText(sizeText)

    def updateSpeed(self, byteLengthPerSecond: int):
        num, unit = byteLengthToHumanReadable(byteLengthPerSecond)
        self.speedLabel.setText(f"{num} {unit}/s")

    @onceMethod
    def switchToImportUi(self):
        """切换到导入阶段的UI"""
        # if self.isImportUi:
            # return
        # self.isImportUi = True
        self.progressLabel.setText("")
        self.speedLabel.setText("解压并导入中……")
        # take走之后还要设置parent为None，不然有进度时会有显示bug
        item = self.progressBarHLayout.takeAt(0)
        item.widget().setParent(None)
        self.progressBarHLayout.insertWidget(0, IndeterminateProgressBar(start=True))

    @onceMethod
    def switchToSuccessUi(self):
        """切换到成功阶段的UI"""
        self.progressLabel.setText("")
        self.speedLabel.setText("安装成功")
        # 移除import ui中的 progress bar
        item = self.progressBarHLayout.takeAt(0)
        item.widget().setParent(None)
        successProgressBar = ProgressBar()
        successProgressBar.setMaximum(1)
        successProgressBar.setValue(1)
        successProgressBar.setCustomBarColor(app_config.SUCCESS_COLOR, app_config.SUCCESS_COLOR)
        self.progressBarHLayout.insertWidget(0, successProgressBar)
    
    @onceMethod
    def switchToErrorUi(self, reason: str):
        """切换到失败阶段的UI"""
        self.progressLabel.setText("")
        self.speedLabel.setText(f"安装失败：{reason}")
        # 移除import ui中的 progress bar
        item = self.progressBarHLayout.takeAt(0)
        item.widget().setParent(None)
        errorProgressBar = ProgressBar()
        errorProgressBar.setMaximum(1)
        errorProgressBar.setValue(1)
        errorProgressBar.setCustomBarColor(app_config.ERROR_COLOR, app_config.ERROR_COLOR)
        self.progressBarHLayout.insertWidget(0, errorProgressBar)

def calculateProgressPercentage(
    completedLength: int, totalLength: int, n: int
) -> float:
    """返回下载进度百分比，保留`n`位小数，取值范围[0, 1]，如果`totalLength`为0则返回0.0"""
    if totalLength != 0:
        percentage = round(completedLength / totalLength, n)
    else:
        percentage = 0.0
    return percentage


def byteLengthToHumanReadable(bytes: int):
    """将字节长度转化为人类可读的形式，返回一个元组`(数量，单位)`"""
    if bytes >= 1024 * 1024 * 1024:
        number = round(bytes / 1024 / 1024 / 1024, 2)
        unit = "GB"
    elif bytes >= 1024 * 1024:
        number = round(bytes / 1024 / 1024, 2)
        unit = "MB"
    elif bytes >= 1024:
        number = round(bytes / 1024, 2)
        unit = "KB"
    else:
        number = bytes
        unit = "B"
    return number, unit


if __name__ == "__main__":
    app = QApplication()
    job = MockModInstallationJob()
    job.mirrorStationNames.append("FrostBlade镜像站")
    window = ModInstallationCardView(job)
    timer = QTimer()
    timer.setInterval(1000)
    timer.timeout.connect(lambda: window.presenter.updateDisplayData())
    timer.start()
    # QTimer.singleShot(2000, window.switchToImportUi)
    # window.switchToSuccessUi()
    # window.switchToErrorUi("abcdefg")
    window.show()
    app.exec()
