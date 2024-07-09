import random
from typing import List
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QApplication,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from features.common.global_objects import Globals
from features.common.mod import ModData
from features.common.mod_installation import (
    CardName,
    MockModInstallationJob,
    ModInstallationStage,
)
from features.common.tricks import Fn
from features.installation.card.view import ModInstallationCardView
from qfluentwidgets import (
    Signal,
    SingleDirectionScrollArea,
)

from features.installation.presenter import ModInstallationPresenter


class InstallationCardsScrollArea(SingleDirectionScrollArea):
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


class DownloadManagerView(QWidget):
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
        self.scrollArea = InstallationCardsScrollArea()
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


# def test1(window: DownloadManagerView):
#     card1 = ModInstallationCardView(MockModInstallationJob())
#     card2 = ModInstallationCardView(MockModInstallationJob())
#     card3 = ModInstallationCardView(MockModInstallationJob())
#     cards = [card1, card2, card3]
#     window.scrollArea.renderCards(cards)
#     card2.presenter.model.stage = ModInstallationStage.importing
#     QTimer.singleShot(2000, lambda: window.scrollArea.renderCards(cards))
#     QTimer.singleShot(3000, lambda: cards.remove(card2))
#     QTimer.singleShot(4000, lambda: window.scrollArea.renderCards(cards))


# def test2(window: DownloadManagerView):
#     window.presenter.enablePollingUpdate()
#     Globals.modInstallationManager.addMockJob(5)
#     # Globals.modInstallationManager.addJob(
#     #     ["https://g-3959.modapi.io/v1/games/3959/mods/2804502/files/5245410/download"],
#     #     CardName("Dust 2", "1"),
#     # )


# def test3(window: DownloadManagerView):
#     Globals.modInstallationManager.addJob(
#         ModData.constructFromServer(2802847), CardName("测试文件", "")
#     )


def test4(window: DownloadManagerView):
    Globals.modInstallationManager.addMockJob(3)


def test5(window: DownloadManagerView):
    card_dl = ModInstallationCardView(MockModInstallationJob(1, 1, True))
    card_dl.presenter.model.stage = ModInstallationStage.downloading
    card_import = ModInstallationCardView(MockModInstallationJob(1, 2, willOccurError=True))
    card_import.presenter.model.stage = ModInstallationStage.importing
    card_success = ModInstallationCardView(MockModInstallationJob(1, 3, willOccurError=True))
    card_success.presenter.model.stage = ModInstallationStage.succeed
    card_error = ModInstallationCardView(MockModInstallationJob(1, 4, willOccurError=True))
    card_error.presenter.model.stage = ModInstallationStage.error
    cards = [card_dl, card_import, card_success, card_error]
    random.shuffle(cards)
    # print(",".join([card.presenter.model.stage.name for card in cards]))
    # cards.sort(key=lambda card: card.presenter.getJob().stage.value)
    # print(",".join([card.presenter.model.stage.name for card in cards]))
    window.presenter.cards = cards
    window.presenter._sortCards()
    print(",".join([card.presenter.model.stage.name for card in cards]))
    window.scrollArea.renderCards(window.presenter.cards)


if __name__ == "__main__":
    app = QApplication()
    window = DownloadManagerView()
    window.presenter.enablePollingUpdate()
    # test1(window)
    # test2(window)
    test4(window)
    # test5(window)

    window.resize(800, 500)
    window.show()
    app.exec()
