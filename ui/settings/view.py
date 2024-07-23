from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import InfoBar, InfoBarPosition

from ui.interfaces.i_refreshable import IRefreshable
from ui.settings.presenter import SettingsPresenter
from ui_design.settings_interface_ui import Ui_SettingsInterface

CLEAN_DOWNLOAD_TMP_TEXT = "清理软件缓存（共计%s）"


class SettingsView(QWidget, Ui_SettingsInterface, IRefreshable):
    def __init__(self) -> None:
        super().__init__()
        self.presenter = SettingsPresenter(self)
        self.setupUi(self)
        self.cleanTmpButton.clicked.connect(self.presenter.cleanTempFile)
        self.openLogDirButton.clicked.connect(self.presenter.openLogDir)

    def refresh(self):
        self.presenter.refreshTmpSize()

    def setTempFilesSize(self, num: float | int, unit: str):
        self.cleanTmpButton.setText(CLEAN_DOWNLOAD_TMP_TEXT % f"{num}{unit}")

    def showCleanTempCompletedInfo(self):
        InfoBar.info(
            title="清理完毕",
            content="",
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=3000,
            parent=self,
        )


if __name__ == "__main__":
    app = QApplication()
    window = SettingsView()
    window.show()
    app.exec()
