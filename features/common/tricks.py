# 写项目时想到一些奇技淫巧，功能大多不完善，注意不要滥用

from functools import wraps
from typing import Callable, Any, Generic, Iterable, List, TypeVar


T = TypeVar("T")
E = TypeVar("E")


class Fn(Generic[T]):
    def __init__(self, func: Callable[..., T]):
        self.func: Callable[..., T] = func

    def call(self) -> T:
        return self.func()

    def repeat(self, n: int) -> None:
        for i in range(n):
            self.func()

    def forEach(self, iter: Iterable[E]) -> None:
        for e in iter:
            self.func(e)


def once(func: Callable[..., T]):
    """
    使用该装饰器后，可以保证该函数只会执行一次，后续将会返回None（且不会抛出异常）"""
    hasCalled = False

    @wraps(func)
    def wrapper(*args, **kwargs) -> T | None:
        nonlocal hasCalled
        if not hasCalled:
            hasCalled = True
            return func(*args, **kwargs)
        else:
            return None

    return wrapper


def onceMethod(func: Callable[..., T]):
    """
    使用该装饰器后，可以保证该函数只会执行一次，后续将会返回None（且不会抛出异常）"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> T | None:
        self = args[0]
        attr = f"__hasCalled_{func.__name__}"
        if not hasattr(self, attr):
            setattr(self, attr, True)
            return func(*args, **kwargs)
        else:
            return None

    return wrapper


def cached(func: Callable[..., T]):
    """使用该装饰器后，可以该函数只会执行一次，后续将会返回缓存的值"""
    hasCalled = False
    cache: T

    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        nonlocal hasCalled, cache
        if not hasCalled:
            hasCalled = True
            cache = func(*args, **kwargs)
        return cache

    return wrapper
