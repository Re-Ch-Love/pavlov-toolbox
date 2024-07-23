from dataclasses import dataclass
from common.mod.installation.mod_name import ModName
from common.mod.mod_data import ModData


from typing import List


@dataclass
class ModInstallationInfo:
    """在Mod安装的过程中产生的信息"""

    modData: ModData
    modName: ModName
    mirrorStationNames: List[str]
