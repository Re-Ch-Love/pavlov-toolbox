from typing import Any, Callable, Dict, Type

# _T = TypeVar("_T")


class SingletonNotRegisteredError(Exception):
    """尝试inject未register的单例时抛出"""


class SingletonManager:
    """
    单例管理器类，用于注册和注入单例对象。

    可以使用该文件中的globalSingletonManager，也可以构造自己的单例管理器，只要实例化该类即可。
    使用示例：
    ```
    globalSingletonManager.register(object())
    class TestCls:
        @property
        @globalSingletonManager.inject(object)
        def obj(self):
            pass
    ```
    """
    
    def __init__(self) -> None:
        self.persistence: Dict[Type, Any] = {}

    def register(self, obj: Any):
        self.persistence[type(obj)] = obj

    def inject(self, cls: Type):
        if cls not in self.persistence:
            raise SingletonNotRegisteredError(f"{cls} is not registered")

        def decorator(_: Callable):

            def wrapper(*args, **kwargs):
                return self.persistence[cls]

            return wrapper

        return decorator


globalSingletonManager = SingletonManager()
