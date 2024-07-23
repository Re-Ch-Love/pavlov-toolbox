from dataclasses import asdict
from typing import Any, Callable
from PySide6.QtWidgets import QApplication, QSizePolicy, QWidget
from PySide6.QtGui import QColor

from qfluentwidgets import FluentIcon, IndeterminateProgressBar, ProgressBar, themeColor

from common.log import AppLogger
from common.mod.installation.mod_name import ModName
from ui.installation.card import colors
from ui.installation.card.options import ModInstallationCardOptions
from ui_design.installation_card_ui import Ui_InstallationCard


class ModInstallationCardView(QWidget, Ui_InstallationCard):

    DISPLAY_NAME_FORMAT = '<span style=" font-size:16pt;">%s</span>'
    HINT_NAME_FORMAT = '<span style=" font-size:10pt; color:#737373;">（%s）</span>'

    def __init__(
        self,
        opts: ModInstallationCardOptions | None = None,
    ):
        """构造函数

        Args:
            opts (ModInstallationCardOptions | None, optional): 卡片选项，不填或为None则设置为默认值. Defaults to None.
        """
        super().__init__()
        # 初始化UI
        self.setupUi(self)
        self.closeButton.setIcon(FluentIcon.CLOSE)
        self.opts: ModInstallationCardOptions = (
            opts if opts is not None else ModInstallationCardOptions.empty()
        )
        self.progressBar: ProgressBar | IndeterminateProgressBar | None = None
        self.setOptions(self.opts, onlyDiff=False)

    def setOptions(self, newOpts: ModInstallationCardOptions, onlyDiff: bool = True):
        """设置卡片选项

        Args:
            newOpts (ModInstallationCardOptions | None, optional): 新的卡片选项. Defaults to None.
            onlyDiff (bool, optional): 启用时只会对newOpts和之前的opts有差异的地方进行更新. Defaults to True.
        """
        diff: dict[str, Any]
        if onlyDiff:
            diff = ModInstallationCardOptions.diff(self.opts, newOpts, newOpts)
        else:
            diff = asdict(newOpts)
        self.opts = newOpts
        for key, value in diff.items():
            # 将字段名转换为对应的set方法名
            methodName = f"_set{key[0].upper()}{key[1:]}"
            getattr(self, methodName)(value)

    def _removeProgressBarIfExist(self):
        if self.progressBarHLayout.count() != 0:
            item = self.progressBarHLayout.takeAt(0)
            item.widget().setParent(None)

    def _setProgressBarPercentage(self, progressBarPercentage: float):
        # 设置进度条
        if 0 <= progressBarPercentage <= 1:
            # 如果取值在[0, 1]之间，则设置进度百分比
            if not self.progressBar or not isinstance(self.progressBar, ProgressBar):
                self._removeProgressBarIfExist()
                self.progressBar = ProgressBar()
                self.progressBar.setSizePolicy(
                    QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
                )
                self.progressBarHLayout.insertWidget(0, self.progressBar)
                self.progressBar.setMaximum(1000)
            self.progressBar.setValue(round(progressBarPercentage * 1000))
        else:
            # 否则设置为不确定的进度条
            if not self.progressBar or not isinstance(self.progressBar, IndeterminateProgressBar):
                self._removeProgressBarIfExist()
                self.progressBar = IndeterminateProgressBar(start=True)
                self.progressBarHLayout.insertWidget(0, self.progressBar)
                self.progressBar.setSizePolicy(
                    QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
                )

    def _setProgressBarColor(self, progressBarColor: QColor | None):
        if self.progressBar is None:
            return
        # 设置进度条颜色
        if progressBarColor:
            self.progressBar.setCustomBarColor(progressBarColor, progressBarColor)
        else:
            # 恢复默认颜色
            self.progressBar.setCustomBarColor(themeColor(), themeColor())

    def _setModName(self, modName: ModName):
        # 设置卡片名称
        nameLabelText = self.DISPLAY_NAME_FORMAT % modName.mainName
        if modName.hintName:
            nameLabelText += self.HINT_NAME_FORMAT % modName.hintName
        self.nameLabel.setText(nameLabelText)

    def _setCloseButtonClickedCallback(self, closeButtonClickedCallback: Callable[..., Any] | None):
        # 设置关闭按钮
        if closeButtonClickedCallback:
            # 要先断开与之前的槽函数的链接，否则会触发多次
            self.closeButton.clicked.disconnect()
            self.closeButton.clicked.connect(closeButtonClickedCallback)
            self.closeButton.setEnabled(True)
        else:
            self.closeButton.setEnabled(False)

    def _setPrompt(self, prompt: str):
        # 设置提示语
        self.promptLabel.setText(prompt)

    def _setProgressInfo(self, progressInfo: str):
        # 设置进度信息
        self.progressInfoLabel.setText(progressInfo)

    # if job.mirrorStationNames:
    #     mirrorsStationsText = "、".join(job.mirrorStationNames)
    #     self.mirrorStationsLabel.setText(f"通过{mirrorsStationsText}加速下载")
    # else:
    #     self.mirrorStationsLabel.setText("")

    # def updateProgress(self, completedLength: int, totalLength: int):
    #     progressPercentage = calculateProgressPercentage(completedLength, totalLength, 3)
    #     self.progressBar.setValue(round(progressPercentage * self.progressBar.maximum()))
    #     completedNum, completedUnit = byteLengthToHumanReadable(completedLength)
    #     totalNum, totalUnit = byteLengthToHumanReadable(totalLength)
    #     sizeText = f"{completedNum}{completedUnit} / {totalNum}{totalUnit}"
    #     self.progressLabel.setText(sizeText)

    # def updateSpeed(self, byteLengthPerSecond: int):
    #     num, unit = byteLengthToHumanReadable(byteLengthPerSecond)
    #     self.speedLabel.setText(f"{num} {unit}/s")

    # def switchToImportUi(self):
    #     """切换到导入阶段的UI"""

    # self.progressLabel.setText("")
    # self.speedLabel.setText("解压并导入中……")
    # item = self.progressBarHLayout.takeAt(0)
    # # take之后还要设置parent为None，不然有进度时会有显示bug
    # item.widget().setParent(None)
    # self.progressBarHLayout.insertWidget(0, IndeterminateProgressBar(start=True))

    # def switchToSuccessUi(self):
    #     """切换到成功阶段的UI"""
    #     self.progressLabel.setText("")
    #     self.speedLabel.setText("安装成功")
    #     # 移除import ui中的 progress bar
    #     item = self.progressBarHLayout.takeAt(0)
    #     item.widget().setParent(None)
    #     successProgressBar = ProgressBar()
    #     successProgressBar.setMaximum(1)
    #     successProgressBar.setValue(1)
    #     successProgressBar.setCustomBarColor(SUCCESS_COLOR, SUCCESS_COLOR)
    #     self.progressBarHLayout.insertWidget(0, successProgressBar)

    # def switchToErrorUi(self, reason: str):
    #     """切换到失败阶段的UI"""
    #     self.progressLabel.setText("")
    #     self.speedLabel.setText(f"安装失败：{reason}")
    #     # 移除import ui中的 progress bar
    #     item = self.progressBarHLayout.takeAt(0)
    #     item.widget().setParent(None)
    #     errorProgressBar = ProgressBar()
    #     errorProgressBar.setMaximum(1)
    #     errorProgressBar.setValue(1)
    #     errorProgressBar.setCustomBarColor(ERROR_COLOR, ERROR_COLOR)
    #     self.progressBarHLayout.insertWidget(0, errorProgressBar)


if __name__ == "__main__":
    app = QApplication()
    opts = ModInstallationCardOptions(
        modName=ModName("主要名称", "xxx的依赖"),
        closeButtonClickedCallback=lambda: print("closed"),
        progressBarColor=colors.SUCCESS_COLOR,
        progressBarPercentage=-1,
        progressInfo="导入中",
        prompt="通过FrostBlade镜像站加速下载",
    )

    window = ModInstallationCardView(opts)
    window.show()
    app.exec()
