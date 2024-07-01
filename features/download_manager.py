from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from aria2.aria2 import Aria2
from features.download_card import DownloadCard
from qfluentwidgets import SingleDirectionScrollArea


class DownloadCardScrollArea(SingleDirectionScrollArea):
    """下载卡片的滚动区域"""

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
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        for n in range(10):
            self.qVBoxLayout.addWidget(DownloadCard(f"测试文件{n+1}", ""))
        self.setWidget(self.view)


class DownloadManagerInterface(QWidget):
    def __init__(self, aria2: Aria2):
        super().__init__()
        self.aria2 = aria2
        self.mainQVBoxLayout = QVBoxLayout(self)
        self.downloadCardScrollArea = DownloadCardScrollArea()
        self.mainQVBoxLayout.addWidget(self.downloadCardScrollArea)
        self.setObjectName(self.__class__.__name__)

    # def updateCards()


if __name__ == "__main__":
    app = QApplication()
    aria2 = Aria2()
    window = DownloadManagerInterface(aria2)
    window.resize(500, 300)
    window.show()
    app.exec()
