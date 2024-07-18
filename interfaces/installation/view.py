import random
from typing import List
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QApplication,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from common.mod.mod_data import ModData
from common.mod.mod_installation import (
    CardName,
    MockModInstallationJob,
    ModInstallationManager,
    ModInstallationStage,
)

from qfluentwidgets import (
    InfoBar,
    Signal,
    SingleDirectionScrollArea,
    SubtitleLabel,
)

from interfaces.installation.card.view import ModInstallationCardView
from interfaces.installation.presenter import ModInstallationPresenter


class InstallationCardsScrollArea(SingleDirectionScrollArea):
    def __init__(self) -> None:
        super().__init__(orient=Qt.Orientation.Vertical)
        self.setWidgetResizable(True)
        # scrollArea 中的容器 widget
        self.view = QWidget(self)
        self.view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # 设置透明背景
        self.setStyleSheet("QScrollArea{background: transparent; border: none}")
        # 文档说必须给内部的视图也加上透明背景样式
        self.view.setStyleSheet("QWidget{background: transparent}")

        # self.view.setStyleSheet("background-color:red;")  # 调试用
        self.qVBoxLayout = QVBoxLayout(self.view)
        self.qVBoxLayout.addStretch(1)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setWidget(self.view)

    def addCard(self, card: ModInstallationCardView):
        self.qVBoxLayout.insertWidget(self.qVBoxLayout.count() - 1, card)

    # def removeCard(self, card: ModInstallationCardView):
    #     self.qVBoxLayout.removeWidget(card)

    def renderCards(self, cards: List[ModInstallationCardView]):
        """清除现有卡片，然后根据传入的card重绘"""
        # 隐藏现有卡片
        # 遍历所有的card, count() - 1是因为最后一个元素是个Spacer
        for _ in range(self.qVBoxLayout.count() - 1):
            # take会取出当前的卡片，所以只要一直取第一个就行了
            item = self.qVBoxLayout.takeAt(0)
            item.widget().hide()
        for card in cards:
            card.presenter.updateDisplayData()
            self.addCard(card)
            card.show()

    # def updateCards(self):
    #     for i in range(self.qVBoxLayout.count() - 1):
    #         widget = self.qVBoxLayout.itemAt(i).widget()
    #         if isinstance(widget, ModInstallationCardView):
    #             widget.presenter.updateDisplayData()


class ModInstallationManagerView(QWidget):
    showStatusChanged = Signal(bool)
    """
    父级窗口切换到该界面时，发送该信号。
    
    传递的值为`DownloadManagerInterface是否为当前显示出来的界面`。
    如果True，则该类会轮询aria2来更新进度等信息。
    如果False，则停止轮询以节省资源。

    注意：父级窗口不会保留状态信息，所以每次切换窗口时，都会发射一个True或False，因此该类需要自己保存这个状态以供比较是否是活跃界面。
    """

    def __init__(self):
        super().__init__()
        self.presenter = ModInstallationPresenter(self)
        self.mainQVBoxLayout = QVBoxLayout(self)
        # self.titleLabel = SubtitleLabel(self)
        # self.titleLabel.setText("管理Mod安装任务")
        # self.titleLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # self.mainQVBoxLayout.addWidget(self.titleLabel)
        self.scrollArea = InstallationCardsScrollArea()
        self.scrollArea.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.mainQVBoxLayout.addWidget(self.scrollArea)
        self.isShow = False
        self.showStatusChanged.connect(self._onShowStatusChanged)
        self.setObjectName(self.__class__.__name__)

    def _onShowStatusChanged(self, newStatus: bool):
        # 如果状态不一样，说明切换了；如果一样，忽略。
        if newStatus != self.isShow:
            self.isShow = newStatus
            if newStatus:
                self.presenter.enablePollingUpdate()
            else:
                self.presenter.disablePollingUpdate()


def test1():
    """测试下载有依赖和镜像源的Mod"""
    app = QApplication()
    window = ModInstallationManagerView()
    window.presenter.enablePollingUpdate()
    manager = ModInstallationManager.getInstance()
    # 这是一个有依赖的Mod
    # mod = ModData.constructFromServer(3243988)
    # manager.addJob(mod, installedCheck=False)
    manager.addMockJob(1)
    window.show()
    app.exec()


if __name__ == "__main__":
    test1()
