import random
from typing import List, cast
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from common.log import AppLogger, logThis
from common.mod.installation.mod_download_manager import (
    ModDownloadManager,
)


from common.mod.installation.mod_name import ModName
from common.mod.mod_data import ModData
from ui.installation.card import colors
from ui.installation.card.options import ModInstallationCardOptions
from ui.installation.card.view import ModInstallationCardView
from ui.installation.scroll_area import InstallationCardsScrollArea
from ui.interfaces.i_freezable import IFreezable
from ui.interfaces.i_refreshable import IRefreshable
from ui.installation.presenter import ModInstallationPresenter


class ModInstallationManagerView(QWidget, IRefreshable, IFreezable):

    def __init__(self):
        super().__init__()
        self.presenter = ModInstallationPresenter(self)
        self.mainQVBoxLayout = QVBoxLayout(self)
        self.scrollArea = InstallationCardsScrollArea()
        self.scrollArea.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.mainQVBoxLayout.addWidget(self.scrollArea)
        self.setObjectName(self.__class__.__name__)

    def refresh(self):
        # AppLogger().debug("ModInstallationManagerView refresh")
        self.presenter.isShow = True

    def freeze(self):
        # AppLogger().debug("ModInstallationManagerView freeze")
        self.presenter.isShow = False

    def renderCards(self, optsList: List[ModInstallationCardOptions]):
        # VBox中还有一个弹簧，因此要-1
        cardCount = self.scrollArea.qVBoxLayout.count() - 1
        # 如果现有的卡片比optsList的长度多，则清除多余的，反之补齐
        if cardCount > len(optsList):
            for _ in range(self.scrollArea.qVBoxLayout.count() - 1 - len(optsList)):
                # take会取出当前的卡片，所以只要一直取第一个就行了
                item = self.scrollArea.qVBoxLayout.takeAt(0)
                item.widget().setParent(None)
        elif cardCount < len(optsList):
            for _ in range(len(optsList) - cardCount):
                card = ModInstallationCardView()
                self.scrollArea.addCard(card)

        # 根据传入的opts列表渲染新的卡片
        for index, opts in enumerate(optsList):
            card = cast(ModInstallationCardView, self.scrollArea.qVBoxLayout.itemAt(index).widget())
            card.setOptions(opts)


def test1():
    """测试动态改变卡片进度"""
    app = QApplication()
    window = ModInstallationManagerView()
    # 这是一个有依赖的Mod
    opts1 = ModInstallationCardOptions(
        progressBarPercentage=0,
        progressBarColor=None,
        modName=ModName("主要名称", "xxx的依赖"),
        closeButtonClickedCallback=None,
        prompt="",
        progressInfo="",
    )
    window.renderCards([opts1])

    timer = QTimer()
    timer.setInterval(1000)

    def increaseProgress():
        opts1.progressBarPercentage += 0.1
        window.renderCards([opts1])

    timer.timeout.connect(increaseProgress)
    timer.start()
    window.show()
    app.exec()


def test2():
    """测试动态改变卡片数量"""
    app = QApplication()
    window = ModInstallationManagerView()
    # 这是一个有依赖的Mod
    optsList = []
    timer = QTimer()
    timer.setInterval(1000)

    def changeCount():
        # 如果列表不为空，那么1/4概率删除一个card
        if len(optsList) != 0 and random.randint(0, 3) == 0:
            # 随机删除一个card
            optsList.pop(random.randint(0, len(optsList) - 1))
        else:
            # 随机位置插入一个card
            optsList.insert(random.randint(0, len(optsList)), ModInstallationCardOptions.empty())
        for index, opts in enumerate(optsList):
            opts.progressBarPercentage += random.uniform(0, 0.3)
            opts.modName = ModName(
                f"我是第{index}个", f"我的进度是{round(opts.progressBarPercentage * 100, 1)}%"
            )
        window.renderCards(optsList)

    changeCount()
    timer.timeout.connect(changeCount)
    timer.start()
    window.show()
    app.exec()


def test3():
    """测试下载有依赖和镜像站的Mod"""
    app = QApplication()
    window = ModInstallationManagerView()
    window.refresh()
    # 这是一个有依赖的Mod
    mod = ModData.constructFromApi(3243988)
    ModDownloadManager.getInstance().addTask(mod, isCheckInstallationStatus=False)
    window.show()
    app.exec()


def test4():
    """测试第一个卡片正在下载，第二个卡片成功，然后关闭第二个卡片，能否正常显示"""
    app = QApplication()
    window = ModInstallationManagerView()
    opts1 = ModInstallationCardOptions.empty()
    opts2 = ModInstallationCardOptions.empty()
    optsList = [opts1, opts2]

    def removeCard(opts):
        optsList.remove(opts)
        window.renderCards(optsList)

    opts1.progressBarPercentage = 0.5
    opts2.progressBarPercentage = 1
    opts2.progressBarColor = colors.SUCCESS_COLOR
    opts2.closeButtonClickedCallback = lambda: removeCard(opts2)

    window.renderCards(optsList)
    window.show()
    app.exec()


if __name__ == "__main__":
    test4()
