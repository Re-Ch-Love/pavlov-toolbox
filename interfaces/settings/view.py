import os
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import InfoBar, InfoBarPosition

from interfaces.installation.card.view import byteLengthToHumanReadable
from ui_design.settings_interface_ui import Ui_SettingsInterface

CLEAN_DOWNLOAD_TMP_TEXT = "清理下载文件缓存（共计%s）"


class SettingsView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_SettingsInterface()
        self.ui.setupUi(self)
        self.ui.cleanDownloadTmpButton.clicked.connect(self.cleanDownloadTmp)
        self.refreshDownloadTmpSize()

    def refreshDownloadTmpSize(self):
        totalSize = 0
        for dirpath, _, filenames in os.walk("downloads"):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                totalSize += os.path.getsize(fp)
        totalNum, totalUnit = byteLengthToHumanReadable(totalSize)
        self.ui.cleanDownloadTmpButton.setText(
            CLEAN_DOWNLOAD_TMP_TEXT % f"{totalNum}{totalUnit}"
        )

    def cleanDownloadTmp(self):
        for dirpath, _, filenames in os.walk("downloads"):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                os.remove(fp)

        InfoBar.info(
            title="清理完毕",
            content="",
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=3000,
            parent=self,
        )
        self.refreshDownloadTmpSize()

if __name__ == "__main__":
    app = QApplication()
    window = SettingsView()
    window.show()
    # app.exec()
