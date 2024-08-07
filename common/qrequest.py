from enum import Enum
from typing import Any, Callable, List, Self
from PySide6 import QtNetwork
from PySide6 import QtCore
from PySide6.QtCore import QObject
from PySide6.QtNetwork import QNetworkAccessManager
from PySide6.QtWidgets import QApplication

from common.log import logThis
from common.tricks import interfaceMethod


class GlobalQNetworkAccessManager:
    """全局网络访问管理器

    使用单例模式，每次new出来都是同一个实例。
    """

    _instance: QNetworkAccessManager | None = None

    @staticmethod
    def get():
        if GlobalQNetworkAccessManager._instance is None:
            GlobalQNetworkAccessManager._instance = QNetworkAccessManager()
        return GlobalQNetworkAccessManager._instance


class QRequestMode(Enum):
    GET = 1
    POST = 2
    PUT = 3


class QPromise:
    """QPromise基类

    对于一个QPromise，调用其then方法可以附加一个处理函数。

    如果上一个then函数是网络请求等需要过一段时间才能处理完的操作，
    则新添加的then函数会附加到上一个then函数后面。
    """

    def __init__(self):
        self.thenFuncList: List[Callable[..., Any]] = []
        self.catchFunc: Callable[..., Any] | None = None
        # 如果定义了final，需要考虑：
        # 当thenFunc的链式调用中返回了QPromise时，如果该QPromise已经有了finalFunc，那么外层的finalFunc就需要放到这个finalFunc之后去执行
        # 实现起来比较复杂，而且暂时不需要，因此搁置
        # self.finalFunc: Callable[..., Any] | None = None

    def then(self, func: Callable[..., Any]) -> Self:
        self.thenFuncList.append(func)
        return self

    def catch(self, func: Callable[..., Any]) -> Self:
        self.catchFunc = func
        return self

    # def final(self, func: Callable[..., Any]) -> Self:
    #     self.finalFunc = func
    #     return self

    @interfaceMethod
    def done(self) -> Self: ...


class QPromiseError(Exception):
    pass


class QRequestPromiseNoCatchFuncError(QPromiseError):
    def __init__(self, error: QtNetwork.QNetworkReply.NetworkError):
        self.error = error

    def __str__(self) -> str:
        return f"error {self.error.name} occurred, but no catch func provided"


class QRequestPromise(QObject, QPromise):
    """请求Promise

    封装了Qt网络请求相关的调用，使用方法详见`QRequestReady`
    """

    def __init__(self, parent: QObject, mode: QRequestMode, url: str):
        super().__init__(parent)
        self.url: str = url
        self.mode = mode
        self.lastFuncResult: Any = None

    def then(self, func: Callable[..., Any]) -> Self:
        self.thenFuncList.append(func)
        return self

    def catch(self, func: Callable[..., Any]) -> Self:
        self.catchFunc = func
        return self

    def done(self) -> Self:
        naManager = GlobalQNetworkAccessManager().get()
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(self.url))
        match self.mode:
            case QRequestMode.GET:
                self.reply = naManager.get(request)
            case QRequestMode.POST:
                raise NotImplementedError("QRequest POST not implemented")
            case QRequestMode.PUT:
                raise NotImplementedError("QRequest PUT not implemented")
        self.reply.finished.connect(self.onFinished)
        self.reply.errorOccurred.connect(self.onErrorOccurred)
        return self

    def onFinished(self) -> None:
        if self.reply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
            return
        content = bytes(self.reply.readAll().data())
        self.lastFuncResult: Any = content
        for index, thenFunc in enumerate(self.thenFuncList):
            self.lastFuncResult = thenFunc(self.lastFuncResult)
            # 如果这个函数返回的也是QPromise，则不再执行后续的thenFunc
            # 而是把后续的thenFunc全部放到这个QPromise中
            # 等这个QPromise执行完毕，再由它去执行后续的thenFunc
            if isinstance(self.lastFuncResult, QPromise):
                self.lastFuncResult.thenFuncList.extend(self.thenFuncList[index + 1 :])
                self.lastFuncResult.done()
                break
        self.reply.deleteLater()

    def onErrorOccurred(self, error: QtNetwork.QNetworkReply.NetworkError) -> None:
        if self.catchFunc:
            result = self.catchFunc(error)
        else:
            raise QRequestPromiseNoCatchFuncError(error)
        self.reply.deleteLater()


class QDataPromise(QPromise):
    def __init__(self, data: Any):
        self.data = data
        self.thenFuncList: List[Callable[..., Any]] = []
        self.catchFunc: Callable[[QtNetwork.QNetworkReply.NetworkError], Any] | None = None
        self.lastFuncResult = None

    def then(self, func: Callable[..., Any]) -> Self:
        self.thenFuncList.append(func)
        return self

    def catch(self, func: Callable[[QtNetwork.QNetworkReply.NetworkError], Any]) -> Self:
        self.catchFunc = func
        return self

    def done(self) -> Self:
        self.lastFuncResult: Any = self.data
        for index, thenFunc in enumerate(self.thenFuncList):
            self.lastFuncResult = thenFunc(self.lastFuncResult)
            if isinstance(self.lastFuncResult, QPromise):
                self.lastFuncResult.thenFuncList.extend(self.thenFuncList[index + 1 :])
                self.lastFuncResult.done()
                break
        return self


# 这个类必须要继承QObject，QRequestPromise也一样，否则Qt会把它们清理掉，导致回调无法正常使用
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

    其中then可以附加多个，前一个的返回值将作为后一个的参数。
    由于网络请求需要时间，因此done函数调用后再附加then一般也可以正常运行。
    但安全起见，建议封装功能函数中把自己的then附加上即可，catch和done都交给调用者来执行。
    """

    def __init__(self, parent: QObject):
        super().__init__(parent)

    def get(self, url: str) -> QRequestPromise:
        return QRequestPromise(self, QRequestMode.GET, url)

    def post(self, url: str) -> QRequestPromise:
        return QRequestPromise(self, QRequestMode.POST, url)

    def put(self, url: str) -> QRequestPromise:
        return QRequestPromise(self, QRequestMode.PUT, url)


def test1():
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


def test2():
    """测试能否正确传递返回值"""
    app = QApplication()

    def getResult():
        return QRequestReady(app).get("https://www.example.com").then(lambda content: "some value")

    getResult().then(lambda value: print(value)).catch(lambda error: print(error)).done()
    app.exec()


def test3():
    # 测试在then中返回QPromise
    app = QApplication()
    # 创建一个请求，在then中返回访问baidu的promise，所以这里应该会打印出baidu网页
    request = QRequestReady(app)
    (
        request.get("https://www.example.com")
        .then(lambda _: request.get("https://www.baidu.com"))
        .then(lambda content: print(content.decode()))
        .done()
    )
    print("不阻塞")
    app.exec()


if __name__ == "__main__":
    test1()
    # test2()
    # test3()
