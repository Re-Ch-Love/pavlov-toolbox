from hmac import new
from re import I
from typing import List
from PySide6.QtCore import QTimer

from features.common.globals_objects import Globals
from features.installation.card.view import ModInstallationCardView


class ModInstallationPresenter:
    def __init__(self, view) -> None:
        from features.installation.view import DownloadManagerView

        self.view: DownloadManagerView = view

        # 创建卡片列表
        self.cards: List[ModInstallationCardView] = []
        # 创建一个间隔1000ms的Timer
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.pollingUpdate)

    def pollingUpdate(self):
        # self.view.scrollArea.updateCards()
        # 获取当前的jobs和本地jobs的集合
        currentJobs = set(Globals.modInstallationManager.getAllJobs())
        localJobs = set([card.presenter.getJob() for card in self.cards])
        # 从当前的jobs 减去 本地jobs，就是新增的jobs
        newJobs = currentJobs - localJobs
        # print(f"newJob count: {len(newJobs)}")
        if len(newJobs) != 0:
            for newJob in newJobs:
                self.cards.append(ModInstallationCardView(newJob))
        # 从本地jobs 减去 当前的jobs，就是被删除的jobs
        deletedJobs = localJobs - currentJobs
        # print(f"deletedJob count:{len(deletedJobs)}")
        # 如果有需要删除的Jobs，则删除对应的Card
        if len(deletedJobs) != 0:
            for card in self.cards:
                if card.presenter.getJob() in deletedJobs:
                    self.cards.remove(card)
        
        self._sortCards()
        self.view.scrollArea.renderCards(self.cards)

    def _sortCards(self):
        """
        为卡片进行排序

        顺序：
        - 正在下载的卡片
        - 正在导入的卡片
        - 其他卡片
        """
        self.cards.sort(key=lambda card: card.presenter.getJob().stage.value, reverse=True)

    def enablePollingUpdate(self):
        self.timer.start()

    def disablePollingUpdate(self):
        self.timer.stop()
