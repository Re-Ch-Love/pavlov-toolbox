from functools import wraps
import logging
import os
import sys
import traceback
from typing import Callable, cast
import app_config
import inspect


_appLogger: logging.Logger | None = None
LOG_FORMAT = (
    "%(asctime)s %(pathname)s:%(lineno)s:%(funcName)s in %(threadName)s [%(levelname)s] %(message)s"
)


def initAppLogEnvironment():
    """初始化App日志环境

    该函数做的事情：
    - 初始化AppLogger
    - 对rootLogger进行一些配置
    - 创建日志的存放目录（如果不存在）
    - 替换默认的未捕获异常处理器，让未捕获的异常能够被记录到日志中

    具体行为过多，见代码及注释。
    """

    # 定义异常处理器，使得发生异常后能够将异常的堆栈信息计入到日志中
    def exceptHook(excType, excValue, excTraceback):
        details = "".join(traceback.format_exception(excType, excValue, excTraceback))
        AppLogger().fatal(f"未捕获的异常：\n{details}")

    # 替换默认的异常处理器
    sys.excepthook = exceptHook  # cSpell: disable-line

    # 递归创建日志文件的存放目录（如果不存在）
    os.makedirs(app_config.LOG_DIR, exist_ok=True)
    if app_config.DEBUG:
        # 如果是debug模式，则将日志输出到控制台
        logging.basicConfig(
            format=LOG_FORMAT,
            level=logging.WARN,  # 设置默认等级为WARN
        )
    else:
        # 如果不是debug模式，则将日志输出到日志文件
        logging.basicConfig(
            format=LOG_FORMAT,
            level=logging.WARN,  # 设置默认等级为WARN
            filename=app_config.LOG_FILE_PATH,
            filemode="a",
            encoding="utf-8",
        )

    global _appLogger
    _appLogger = logging.getLogger("app")
    # 设置appLogger的等级为DEBUG或是INFO，取决于app_config.DEBUG的值。
    # 这里的等级不受basicConfig的影响，basicConfig只影响没有指定等级的Logger
    _appLogger.setLevel(logging.DEBUG if app_config.DEBUG else logging.INFO)
    logAppConfig()


def logAppConfig():
    # 打印app_config中定义的常量
    for key in dir(app_config):
        # 如果key中除了下划线以外都是大写字母，则认为它是常量
        if key.replace("_", "").isupper():
            AppLogger().info(f"app_config.{key}={getattr(app_config, key)}")


def AppLogger() -> logging.Logger:
    """获取AppLogger

    Returns:
        logging.Logger: appLogger
    """
    if _appLogger is None:
        initAppLogEnvironment()
        # 初始化之后，_appLogger不再会是None
        cast(logging.Logger, _appLogger).warning(
            "获取AppLogger前没有初始化，请在App启动时第一步就使用log.initAppLogEnvironment()进行初始化！"
        )
    return cast(logging.Logger, _appLogger)


def logThis(func: Callable):
    """日志装饰器

    当app_config.DEBUG为True时，将函数的调用者，入参和返回值等信息记录到日志中（Debug等级），
    否则返回原始函数。
    """
    # 如果不是DEBUG模式，直接返回原始函数
    if not app_config.DEBUG:
        return func

    @wraps(func)
    # 因为这个包装函数里会输出日志，而日志中会显示调用者的名字，所以把wrapper的名字写的详细一些
    def logThisWrapper(*args, **kwargs):
        callerFrame = inspect.stack()[1]
        # 调用者信息
        callerFile = callerFrame[1]
        callerLine = callerFrame[2]
        callerName = callerFrame[3]
        # 函数字节码
        funcCode = func.__code__
        # 将函数的参数名称与值对应成一个dict
        argsDict = dict(zip(funcCode.co_varnames, args))  # cSpell: disable-line
        # 将argsDict和kwargs合并成一个字典
        argsDict.update(kwargs)
        # 从字典中去掉self参数，日志中没必要关心self的实参
        argsDict.pop("self", None)
        # 获取func定义的位置
        funcDefFile = funcCode.co_filename
        funcDefLine = funcCode.co_firstlineno  # cSpell: disable-line
        # 生成一个简短的标识符用于识别Return日志的位置
        callIdentifier = os.urandom(4).hex()  # cSpell: disable-line
        # 在每行前面加上logThis的标记，否则看起来太像堆栈跟踪了
        callMsg = "\n    ".join(
            [
                f"Log function calling with identifier <{callIdentifier}>:",
                f'Calling {func.__name__} (file "{funcDefFile}", line {funcDefLine})',
                f'from {callerName} (file "{callerFile}", line {callerLine})',
                f"with {argsDict}",
            ]
        )

        AppLogger().debug(callMsg)
        result = func(*args, **kwargs)
        returnMsg = "\n    ".join(
            [
                f"Log function returned with identifier <{callIdentifier}>:",
                f'{func.__name__} (file "{funcDefFile}", line {funcDefLine})',
                f"returned {result}",
            ]
        )
        AppLogger().debug(returnMsg)
        return result

    return logThisWrapper


if __name__ == "__main__":

    @logThis
    def simpleFunction():
        pass

    initAppLogEnvironment()
    logging.getLogger("myLogger").info("myLogger: info")
    AppLogger().debug("debug log")
    AppLogger().info("info log")
    simpleFunction()
