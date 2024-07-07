from functools import wraps
from typing import Any, Callable, TypeVar


T = TypeVar("T")


def once(func: Callable[..., T]):
    """使用该装饰器后，可以保证该函数只会执行一次，后续将会返回None（而不是抛出异常）"""
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
