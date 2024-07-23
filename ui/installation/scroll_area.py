from ui.installation.card.options import ModInstallationCardOptions
from ui.installation.card.view import ModInstallationCardView


from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from qfluentwidgets import SingleDirectionScrollArea


from typing import List, cast


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
