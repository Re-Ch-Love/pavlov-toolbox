from common.tricks import interfaceMethod


class IRefreshable:
    """可刷新接口类

    如果一个界面（interface）可刷新，那么可以在切换到该界面时调用其refresh方法来刷新界面上的东西

    注意：实现IRefreshable接口的界面可以不在init中初始化界面上的数据，因为refresh方法会在界面切换时调用
    """

    @interfaceMethod
    def refresh(self) -> None:
        pass
