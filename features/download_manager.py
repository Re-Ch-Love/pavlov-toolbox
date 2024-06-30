from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from features.download_card import DownloadCard

class DownloadManagerInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.qVBoxLayout = QVBoxLayout(self)
        self.card = DownloadCard("测试文件")
        self.qVBoxLayout.addWidget(self.card, stretch=1)
        self.qVBoxLayout.addWidget(DownloadCard("测试文件2"), stretch=1)
        self.qVBoxLayout.addWidget(DownloadCard("测试文件3"), stretch=1)
        self.qVBoxLayout.addStretch(1)
        self.setObjectName(self.__class__.__name__)


if __name__ == "__main__":
    app = QApplication()
    window = DownloadManagerInterface()
    window.resize(500, 300)
    window.show()
    app.exec()