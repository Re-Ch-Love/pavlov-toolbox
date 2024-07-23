import os
import sys

from common.version import Version
from datetime import datetime

VERSION = Version(0, 3, 0)

# 是否为debug模式，通过参数中是否有`--debug`来判断
DEBUG = "--debug" in sys.argv


# 临时目录
TEMP_DIR = os.path.join(os.getenv("TEMP", ""), "PavlovToolboxTemp")
# （临时目录下）临时下载目录
TEMP_DOWNLOAD_DIR = os.path.join(TEMP_DIR, "downloads")
# （临时目录下）导入模组时的临时目录
TEMP_IMPORT_MOD_DIR = os.path.join(TEMP_DIR, "import_mod")

# 本地数据目录
# cSpell: disable-next-line
DATA_DIR = os.path.join(os.getenv("LOCALAPPDATA", ""), "PavlovToolboxData")
# （本地数据目录下）日志文件目录
LOG_DIR = os.path.join(DATA_DIR, "logs")
# （本地数据目录下）此次的日志文件路径
# 获取当前日期的字符串
LOG_FILE_PATH = os.path.join(LOG_DIR, f"{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log")
