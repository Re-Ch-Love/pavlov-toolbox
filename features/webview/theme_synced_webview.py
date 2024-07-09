from typing_extensions import deprecated
from PySide6.QtCore import QResource, QUrl, SignalInstance, Slot, Signal
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import QWidget
from qfluentwidgets import QObject, Theme, qconfig, toggleTheme
from qframelesswindow.webengine import FramelessWebEngineView

class ThemeToggleJsBridge(QObject):
    def __init__(self) -> None:
        super().__init__()

    @Slot()
    def toggle(self):
        toggleTheme()
        


JS_TOGGLE_THEME_SYNC = r"""new QWebChannel(qt.webChannelTransport, function (channel) {
    window.bridge = channel.objects.bridge;
})
window.disable_sync = false;
document.getElementById('theme-toggle').addEventListener("click", ()=>{
    if (!window.disable_sync) {
        window.bridge.toggle();
    }
})
function setTheme(theme) {
    if (theme == "Light") {
        console.log("to light")
        document.body.classList.remove('dark');
        localStorage.setItem("pref-theme", 'light');
    } else if (theme == "Dark") {
        console.log("to dark")
        document.body.classList.add('dark');
        localStorage.setItem("pref-theme", 'dark');
    }
}"""

@deprecated("这个类在切换主题后，在某些情况下会闪烁，因此不再使用，改用WebViewInterface")
class ThemeSyncedWebViewInterface(FramelessWebEngineView):
    """点击网页上的#theme-toggle按钮，可以和App自身主题（浅色/深色）同步的WebView"""

    def __init__(self, uniqueName: str, url: str, parent: QWidget) -> None:
        super().__init__(parent)
        self.load(QUrl(url))
        self.setObjectName(self.__class__.__name__ + "_" + uniqueName)
        self.uniqueName = uniqueName
        self.channel = QWebChannel()
        self.bridge = ThemeToggleJsBridge()
        qconfig.themeChanged.connect(self.toggleWebTheme)
        self.channel.registerObject("bridge", self.bridge)
        self.page().setWebChannel(self.channel)

        def runJS():
            # 从 qrc:///qtwebchannel/qwebchannel.js 中加载
            self.page().runJavaScript(
                bytearray(
                    QResource(":/qtwebchannel/qwebchannel.js").uncompressedData().data()
                ).decode()
            )
            self.page().runJavaScript(JS_TOGGLE_THEME_SYNC)

        # 要等页面加载完再runJS
        self.page().loadFinished.connect(runJS)

    def toggleWebTheme(self, theme: Theme):
        self.page().runJavaScript(f"setTheme('{theme.value}');")
