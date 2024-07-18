from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QApplication,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import FluentIcon
from qframelesswindow.webengine import FramelessWebEngineView

from ui_design.app_webview_toolbox_ui import Ui_AppWebviewToolbox

# 禁用主题切换按钮的JS代码
JS_DISABLE_THEME_TOGGLE_BUTTON = r'document.getElementById("theme-toggle").remove();'
# 禁用页面上所有a标签跳转的JS代码
JS_DISABLE_A_TAGS_JUMP = r"""
let aTags = document.getElementsByTagName("a");
Array.prototype.forEach.bind(aTags)(aTag => {
    aTag.addEventListener('click', (event) => { event.preventDefault(); });
});
"""


class PavlovToolboxWebsiteInterface(QWidget):
    """适配pavlov toolbox网站的webview，会去掉主题切换按钮"""

    def __init__(
        self,
        uniqueName: str,
        url: str,
        parent: QWidget | None = None,
        isRemoveToolButtons: bool = False,
        disableATagsJump: bool = False,
    ) -> None:
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__ + "_" + uniqueName)
        self.initialQUrl = QUrl(url)
        self.webview = FramelessWebEngineView(self)
        self.webview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.outerVBoxLayout = QVBoxLayout(self)
        # 设置无边距
        self.outerVBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.outerVBoxLayout.setSpacing(0)
        if not isRemoveToolButtons:
            self.toolboxWidget = QWidget(self)
            self.toolboxWidget.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum
            )
            # 初始化toolbox ui
            self.toolbox = Ui_AppWebviewToolbox()
            self.toolbox.setupUi(self.toolboxWidget)
            # 设置地址栏文字
            self.toolbox.label.setText(self.initialQUrl.url())
            self.webview.urlChanged.connect(lambda qUrl: self.toolbox.label.setText(qUrl.url()))
            # 初始化按钮
            self.toolbox.homeButton.setIcon(FluentIcon.HOME)
            self.toolbox.backButton.setIcon(FluentIcon.LEFT_ARROW)
            self.toolbox.forwardButton.setIcon(FluentIcon.RIGHT_ARROW)
            # 绑定前进后退等事件
            self.toolbox.backButton.clicked.connect(self.webview.back)
            self.toolbox.forwardButton.clicked.connect(self.webview.forward)
            self.toolbox.homeButton.clicked.connect(lambda: self.webview.load(self.initialQUrl))
            self.outerVBoxLayout.addWidget(self.toolboxWidget)

        self.outerVBoxLayout.addWidget(self.webview)
        self.webview.load(QUrl(self.initialQUrl))
        # 要等页面加载完才能运行JS，不然找不到DOM
        self.webview.page().loadFinished.connect(self.removeThemeToggleButton)
        if disableATagsJump:
            self.webview.page().loadFinished.connect(self.disableATagsJump)

    def removeThemeToggleButton(self):
        self.webview.page().runJavaScript(JS_DISABLE_THEME_TOGGLE_BUTTON)

    def disableATagsJump(self):
        self.webview.page().runJavaScript(JS_DISABLE_A_TAGS_JUMP)


def test1():
    """测试隐藏工具栏和禁用a标签跳转是否正常工作"""
    app = QApplication()
    window = PavlovToolboxWebsiteInterface(
        "test",
        "https://pavlov-toolbox.rech.asia/app-home",
        isRemoveToolButtons=True,
        disableATagsJump=True,
    )
    window.show()
    app.exec()


def test2():
    """测试是否可以正常加载工具栏"""
    app = QApplication()
    window = PavlovToolboxWebsiteInterface(
        "test",
        "https://pavlov-toolbox.rech.asia/app-home",
        isRemoveToolButtons=False,
        disableATagsJump=False,
    )
    window.show()
    app.exec()


if __name__ == "__main__":
    # test1()
    test2()
