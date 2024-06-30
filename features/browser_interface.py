from PySide6.QtCore import QResource, QUrl, Slot
from PySide6.QtWebChannel import QWebChannel
from qfluentwidgets import QObject, toggleTheme
from qframelesswindow.webengine import FramelessWebEngineView


class ToggleThemeBridge(QObject):
    @Slot()
    def toggle(self):
        toggleTheme()

JS_CONTENT = r"""new QWebChannel(qt.webChannelTransport, function (channel) {
    window.bridge = channel.objects.bridge;
})
document.getElementById('theme-toggle').addEventListener("click", ()=>{window.bridge.toggle()})"""

class ThemeSyncedWebViewInterface(FramelessWebEngineView):
    """点击网页上的#theme-toggle按钮，可以和App自身主题（浅色/深色）同步的WebView"""
    def __init__(self, uniqueName: str, url: str, parent) -> None:
        super().__init__(parent)
        self.load(QUrl(url))
        self.setObjectName(self.__class__.__name__ + "_" + uniqueName)
        self.channel = QWebChannel()
        self.bridge = ToggleThemeBridge()
        self.channel.registerObject("bridge", self.bridge)
        self.page().setWebChannel(self.channel)
        def runJS():
            # 从 qrc:///qtwebchannel/qwebchannel.js 中加载
            self.page().runJavaScript(bytearray(QResource(":/qtwebchannel/qwebchannel.js").uncompressedData().data()).decode())
            self.page().runJavaScript(JS_CONTENT)
        # 要等页面加载完再runJS
        self.page().loadFinished.connect(runJS)
