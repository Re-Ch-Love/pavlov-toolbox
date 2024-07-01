from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QSizePolicy, QWidget
from ui.download_card_ui import Ui_DownloadCard
from qfluentwidgets import FluentIcon

class DownloadCard(QWidget):
    toggled = Signal(bool)
    closed = Signal()

    def __init__(self, name: str, gid: str):
        super().__init__()
        self.gid = gid
        self.isDownloading = False
        self.ui = Ui_DownloadCard()
        self.ui.setupUi(self)
        self.ui.nameLabel.setText(name)
        self.ui.toggleButton.setIcon(FluentIcon.PAUSE if self.isDownloading else FluentIcon.PLAY)
        self.ui.toggleButton.clicked.connect(self.toggle)
        self.ui.toggleButton.clicked.connect(self.toggled)
        self.ui.closeButton.setIcon(FluentIcon.CLOSE)
        self.ui.closeButton.clicked.connect(self.closed)
        # self.ui.frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def toggle(self):
        if self.isDownloading:
            self.ui.toggleButton.setIcon(FluentIcon.PLAY)
            self.isDownloading = False
        else:
            self.ui.toggleButton.setIcon(FluentIcon.PAUSE)
            self.isDownloading = True


if __name__ == "__main__":
    app = QApplication()
    window = DownloadCard("测试文件", "")
    window.show()
    app.exec()
