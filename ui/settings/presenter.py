import os
import subprocess

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

import app_config
from common.utils import byteLengthToHumanReadable


class SettingsPresenter:
    def __init__(self, view) -> None:
        from ui.settings.view import SettingsView

        self.view: SettingsView = view

    def refreshTmpSize(self):
        totalSize = 0
        for dirpath, _, filenames in os.walk(app_config.TEMP_DIR):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                totalSize += os.path.getsize(fp)
        totalNum, totalUnit = byteLengthToHumanReadable(totalSize)
        self.view.setTempFilesSize(totalNum, totalUnit)

    def cleanTempFile(self):
        for dirpath, _, filenames in os.walk(app_config.TEMP_DIR):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                os.remove(fp)
        self.refreshTmpSize()

    def openLogDir(self):
        subprocess.run(["explorer", f"/select,{app_config.LOG_FILE_PATH}"])
