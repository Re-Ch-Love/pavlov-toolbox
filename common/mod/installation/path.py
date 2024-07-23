import os
from common.tricks import cached


INI_MOD_DIR_SUFFIX = "ModDirectory="
GAME_SETTING_PATH_BEHIND_HOME = r"AppData\Local\Pavlov\Saved\Config\Windows\GameUserSettings.ini"


class GetModInstallationDirException(Exception):
    """获取Mod安装目录相关异常"""

    def __init__(self, details: str) -> None:
        super().__init__(details)


@cached
def getModInstallationDir() -> str:
    """获取Mod安装目录

    因为考虑到一般不会在打开该App的时候更改Mod安装目录，所以这个函数使用cached装饰器，
    这代表它在整个App的生命周期中只会实际运行一次，后续调用都返回相同的值。
    """
    homePath = os.path.expanduser("~")
    gameUserSettingsPath = os.path.join(homePath, GAME_SETTING_PATH_BEHIND_HOME)
    if not os.access(gameUserSettingsPath, os.F_OK | os.R_OK):
        raise GetModInstallationDirException("文件不存在或无法访问")
    with open(gameUserSettingsPath, "r", encoding="utf-8") as f:
        for line in f:
            if not line.startswith(INI_MOD_DIR_SUFFIX):
                continue
            modDir = line[len(INI_MOD_DIR_SUFFIX) :].strip()
            return modDir
    raise GetModInstallationDirException("无法找到Mod安装目录配置项")