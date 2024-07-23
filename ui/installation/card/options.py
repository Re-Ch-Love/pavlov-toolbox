from dataclasses import asdict, dataclass, field
from functools import partial
from typing import Any, Callable

from qfluentwidgets import QColor

from common.mod.installation.mod_name import ModName
from ui.installation.card import colors


@dataclass
class ModInstallationCardOptions:
    progressBarPercentage: float
    """进度条百分比
    
    取值在[0, 1]中时，显示为普通进度条，并设置为对应的百分比。
    取值在上述范围之外时，显示为不确定进度的进度条。
    """

    progressBarColor: QColor | None
    """进度条颜色"""

    modName: ModName
    """卡片名称
    
    包括主要名称mainName和提示名称hintName
    
    渲染时，提示名称外面会加上括号，如果为空字符串则不渲染"""

    closeButtonClickedCallback: Callable[..., Any] | None
    """关闭按钮点击回调
    
    为空时，会禁用关闭按钮"""

    prompt: str
    """位于卡片左下角的提示语句"""

    progressInfo: str
    """位于卡片右下角的进度信息文本"""

    @staticmethod
    def diff(
        o1: "ModInstallationCardOptions",
        o2: "ModInstallationCardOptions",
        reserve: "ModInstallationCardOptions",
    ) -> dict[str, Any]:
        """比较o1和o2之间的差异，返回值有差异的键在reserve中的值

        Args:
            o1 (ModInstallationCardOptions): 要比较的对象1
            o2 (ModInstallationCardOptions): 要比较的对象2
            reserve (ModInstallationCardOptions): o1和o2中有差异的键在此对象中的值将会被放在字典中返回

        Returns:
            dict[str, Any]: 键为值有差异的属性的名称，值为对应键在reserve中的值

        Examples:
            ```
            opts1 = ModInstallationCardOptions(
                modName=ModName("A", "a"),
                closeButtonClickedCallback=lambda: print("closed"),
                progressBarPercentage=-1,
            )
            opts2 = ModInstallationCardOptions(
                modName=ModName("B", "b"),
                progressBarPercentage=0.5,
            )
            diff = ModInstallationCardOptions.diffBetween(o1=opts1, o2=opts2, reserve=opts2)
            # {
            #     "progressBarPercentage": 0.5,
            #     "modName": ModName(mainName="B", hintName="b"),
            #     "closeButtonClickedCallback": None,
            # }
            ```
        """
        d1 = asdict(o1)
        d2 = asdict(o2)

        return {k: getattr(reserve, k) for k in d1 if d1[k] != d2[k]}

    @classmethod
    def empty(cls) -> "ModInstallationCardOptions":
        return cls(
            progressBarPercentage=0,
            progressBarColor=None,
            modName=ModName("", ""),
            closeButtonClickedCallback=None,
            prompt="",
            progressInfo="",
        )


def test1():
    opts1 = ModInstallationCardOptions(
        progressBarPercentage=-1,
        progressBarColor=None,
        modName=ModName("A", "a"),
        closeButtonClickedCallback=lambda: print("closed"),
        prompt="",
        progressInfo="",
    )
    opts2 = ModInstallationCardOptions(
        progressBarPercentage=0.5,
        progressBarColor=None,
        modName=ModName("B", "b"),
        closeButtonClickedCallback=lambda: print("closed"),
        prompt="",
        progressInfo="",
    )
    diff = ModInstallationCardOptions.diff(o1=opts1, o2=opts2, reserve=opts2)
    print(diff)
    # {
    #     "progressBarPercentage": 0.5,
    #     "modName": ModName(mainName="B", hintName="b"),
    #     "closeButtonClickedCallback": None,
    # }


def test2():
    opts1 = ModInstallationCardOptions.empty()
    opts2 = ModInstallationCardOptions.empty()

    opts1.progressBarPercentage = 0.5
    opts2.progressBarPercentage = 1
    opts2.progressBarColor = colors.SUCCESS_COLOR
    diff = ModInstallationCardOptions.diff(o1=opts1, o2=opts2, reserve=opts2)
    print(diff)


if __name__ == "__main__":
    test2()
