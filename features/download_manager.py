from functools import partial
from typing import Dict, List
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QApplication,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from aria2.aria2 import Aria2
from aria2.aria2_with_data import Aria2WithData
from features.download_card import DownloadCard, CardName
from qfluentwidgets import (
    CardWidget,
    Signal,
    SingleDirectionScrollArea,
    Theme,
    setTheme,
)

from features.download_job import DownloadJob


class DownloadCardsScrollArea(SingleDirectionScrollArea):
    def __init__(self) -> None:
        super().__init__(orient=Qt.Orientation.Vertical)
        self.setWidgetResizable(True)
        # scrollArea 中的容器 widget
        self.view = QWidget(self)
        self.view.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # 设置透明背景
        self.setStyleSheet("QScrollArea{background: transparent; border: none}")
        # 文档说必须给内部的视图也加上透明背景样式
        self.view.setStyleSheet("QWidget{background: transparent}")

        # self.view.setStyleSheet("background-color:red;")  # 调试用
        self.qVBoxLayout = QVBoxLayout(self.view)
        self.qVBoxLayout.addStretch(1)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setWidget(self.view)

    def addWidget(self, widget: QWidget):
        self.qVBoxLayout.insertWidget(self.qVBoxLayout.count() - 1, widget)

    def removeWidget(self, widget: QWidget):
        self.qVBoxLayout.removeWidget(widget)


# FIXME: 下载完成后，进度不是100%，会停留在上一次轮询
class DownloadManagerInterface(QWidget):
    createDownload = Signal(str)

    showStatusChanged = Signal(bool)
    """
    父级窗口切换到该界面时，发送该信号。
    
    传递的值为`DownloadManagerInterface是否为当前显示出来的界面`。
    如果True，则该类会轮询aria2来更新进度等信息。
    如果False，则停止轮询以节省资源。

    注意：父级窗口不会保留状态信息，所以每次切换窗口时，都会发射一个Ture或False，因此该类需要自己保存这个状态以供比较是否时活跃界面。
    """

    def __init__(self, aria2wd: Aria2WithData):
        super().__init__()
        self.aria2wd = aria2wd
        self.mainQVBoxLayout = QVBoxLayout(self)
        self.scrollArea = DownloadCardsScrollArea()
        self.mainQVBoxLayout.addWidget(self.scrollArea)
        self.isShow = False
        self.showStatusChanged.connect(self.onShowStatusChanged)
        self.setObjectName(self.__class__.__name__)
        self.updateTimer = QTimer()
        self.updateTimer.setInterval(1000)
        self.updateTimer.timeout.connect(self.updateCards)
        self.createDownload.connect(self.createDownload)
        self.gidCardMap: Dict[str, DownloadCard] = {}

    def onShowStatusChanged(self, newStatus: bool):
        # 如果状态不一样，说明切换了；如果一样，忽略。
        if newStatus != self.isShow:
            self.isShow = newStatus
            # 如果当前被显示，立刻运行一次，然后启动计时器
            if newStatus:
                self.updateCards()
                self.updateTimer.start()
            else:
                self.updateTimer.stop()

    def updateCards(self):
        rawDownloadJobDatas: List[dict] = self.aria2wd.tellActive(
            DownloadJob.ARIA2_RPC_KEYS + ["gid"]
        )["result"]
        for rawData in rawDownloadJobDatas:
            gid: str = rawData["gid"]
            if gid in self.gidCardMap.keys():
                job = DownloadJob()
                job.loadFromAria2RawData(rawData)
                self.updateCard(gid, job)
            else:
                cardName: CardName = self.aria2wd.getData(gid)
                self.createCard(gid, DownloadCard(cardName))

    def createCard(self, gid: str, card: DownloadCard):
        """创建卡片

        参数`*args`：全部传入`DownloadCard`的构造函数"""
        card.paused.connect(partial(self.aria2wd.pause, gid))
        card.unpaused.connect(partial(self.aria2wd.unpause, gid))
        self.gidCardMap[gid] = card
        self.scrollArea.addWidget(card)

    def deleteCard(self, gid: str):
        targetCard = self.gidCardMap[gid]
        self.scrollArea.removeWidget(targetCard)

    def updateCard(self, gid: str, newJob: DownloadJob):
        targetCard = self.gidCardMap[gid]
        targetCard.updateByNewJob(newJob)


if __name__ == "__main__":
    # setTheme(Theme.DARK)
    app = QApplication()
    aria2 = Aria2WithData()
    window = DownloadManagerInterface(aria2)
    job = DownloadJob()
    job.downloadSpeed = 21414151
    job.completedLength = 21414151
    job.totalLength = job.completedLength * 4
    window.createCard("1", DownloadCard(CardName("Dust 2", "")))
    window.updateCard("1", job)
    window.createCard("2", DownloadCard(CardName("Mod A", "Dust 2 的依赖")))
    window.updateCard("2", job)
    window.createCard("3", DownloadCard(CardName("Mod B", "Dust 2 的依赖")))
    window.updateCard("3", job)

    window.resize(500, 300)
    window.show()
    app.exec()
