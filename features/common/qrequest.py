from enum import Enum
from typing import Callable
from PySide6 import QtNetwork
from PySide6 import QtCore
from PySide6.QtCore import QObject
from PySide6.QtNetwork import QNetworkAccessManager
from PySide6.QtWidgets import QApplication


class GlobalQNetworkAccessManager:
    """全局网络访问管理器

    使用单例模式，无论创建多少个实例，都是同一个实例。
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = QNetworkAccessManager()
        return cls._instance


class QRequest(QObject):
    """请求

    封装了Qt网络请求相关的调用，使用方法详见`QRequestReady`
    """

    class Mode(Enum):
        GET = 1
        POST = 2
        PUT = 3

    def __init__(self, parent: QObject, mode: Mode, url: str):
        super().__init__(parent)
        self.url: str = url
        self.thenFunc: Callable[[bytes], None] | None = None
        self.mode = mode
        self.catchFunc: (
            Callable[[QtNetwork.QNetworkReply.NetworkError], None] | None
        ) = None

    def then(self, func: Callable[[bytes], None]):
        self.thenFunc = func
        return self

    def catch(self, func: Callable[[QtNetwork.QNetworkReply.NetworkError], None]):
        self.catchFunc = func
        return self

    def done(self):
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(self.url))
        match self.mode:
            case QRequest.Mode.GET:
                self.reply = GlobalQNetworkAccessManager().get(request)
            case QRequest.Mode.POST:
                raise NotImplementedError("QRequest POST not implemented")
            case QRequest.Mode.PUT:
                raise NotImplementedError("QRequest PUT not implemented")
        self.reply.finished.connect(self.onFinished)
        self.reply.errorOccurred.connect(self.onErrorOccurred)

    def onFinished(self) -> None:
        if self.reply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
            return
        content = bytes(self.reply.readAll().data())
        if self.thenFunc:
            self.thenFunc(content)
        self.reply.deleteLater()

    def onErrorOccurred(self, error: QtNetwork.QNetworkReply.NetworkError) -> None:
        if self.catchFunc:
            self.catchFunc(error)
        self.reply.deleteLater()


class QRequestReady(QObject):
    """Qt异步请求的封装

    在QRequest之上封装了parent和mode参数，使得使用更加方便，且可以复用RequestReady对象，减少重复代码。

    使用示例：
    ```
    (
        RequestReady(app)
        .get("https://www.example.com")
        .then(lambda content: print("do then"))
        .catch(lambda error: print(f"error: {error.name}"))
        .done()
    )
    ```
    """

    def __init__(self, parent: QObject):
        super().__init__(parent)

    def get(self, url: str) -> QRequest:
        return QRequest(self, QRequest.Mode.GET, url)

    def post(self, url: str) -> QRequest:
        return QRequest(self, QRequest.Mode.POST, url)

    def put(self, url: str) -> QRequest:
        return QRequest(self, QRequest.Mode.PUT, url)


if __name__ == "__main__":
    app = QApplication()
    print("不阻塞1")
    (
        QRequestReady(app)
        .get("https://www.example.com")
        .then(lambda content: print("do then 1"))
        .catch(lambda error: print(f"error: {error.name}"))
        .done()
    )
    print("不阻塞2")
    (
        QRequestReady(app)
        .get("https://www.example.com")
        .then(lambda content: print("do then 2"))
        .catch(lambda error: print(f"error: {error.name}"))
        .done()
    )
    app.exec()
