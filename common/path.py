import os
import sys


def getResourcePath(relativePath: str) -> str:
    """将相对路径转为exe运行时资源文件的绝对路径"""

    if hasattr(sys, "_MEIPASS"):
        # 只有通过exe运行时才会进入这个分支，它返回的是exe运行时的临时目录路径
        basePath = sys._MEIPASS  # type: ignore
    else:
        basePath = os.path.abspath(".")
    return os.path.join(basePath, relativePath)
