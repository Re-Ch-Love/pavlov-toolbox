from typing_extensions import deprecated
from PySide6.QtCore import QResource, QUrl, SignalInstance, Slot, Signal
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import QWidget
from qfluentwidgets import QObject, Theme, qconfig, toggleTheme
from qframelesswindow.webengine import FramelessWebEngineView

class PavlovToolboxWebsiteInterface(FramelessWebEngineView):
    """适配pavlov toolbox网站的webview，会去掉主题调节按钮"""

    def __init__(self, uniqueName: str, url: str, parent: QWidget) -> None:
        super().__init__(parent)
        self.load(QUrl(url))
        self.setObjectName(self.__class__.__name__ + "_" + uniqueName)
        self.uniqueName = uniqueName
        def runJS():
            self.page().runJavaScript('document.getElementById("theme-toggle").remove()')

        # 要等页面加载完再runJS
        self.page().loadFinished.connect(runJS)