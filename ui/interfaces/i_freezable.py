from common.tricks import interfaceMethod


class IFreezable:
    """可冻结的

    如果一个interface是可冻结的，那么在当前显示界面不是该interface时，会调用其freeze方法"""

    @interfaceMethod
    def freeze(self):
        pass
