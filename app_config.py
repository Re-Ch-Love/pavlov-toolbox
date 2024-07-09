import os
from typing import NamedTuple
from PySide6.QtGui import QColor


class Version(NamedTuple):
    x: int
    y: int
    z: int


VERSION = Version(0, 3, 0)
DEBUG = True
TEMP_DIR = os.path.join(os.getenv("TEMP", ""), "pavlov_toolbox_temp")
IMPORT_MOD_TEMP_DIR = os.path.join(TEMP_DIR, "import_mod")
SUCCESS_COLOR = QColor(115, 209, 61)
ERROR_COLOR = QColor(255, 77, 79)
