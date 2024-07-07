import os


class Version:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"{self.x}.{self.y}.{self.z}"

    def __gt__(self, other: "Version") -> bool:
        if isinstance(other, Version):
            # 利用元组来比较
            return (self.x, self.y, self.z) > (other.x, other.y, other.z)
        else:
            return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Version):
            # 利用元组来比较
            return (self.x, self.y, self.z) == (other.x, other.y, other.z)
        else:
            return False


VERSION = Version(0, 2, 0)
DEBUG = True
TEMP_DIR = os.path.join(os.getenv("TEMP", ""), "pavlov_toolbox_temp")
IMPORT_MOD_TEMP_DIR = os.path.join(TEMP_DIR, "import_mod")