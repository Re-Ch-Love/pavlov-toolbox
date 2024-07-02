from typing import Any, Dict
from aria2.aria2 import Aria2


class Aria2WithData(Aria2):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.gidCardNameMap: Dict[str, Any] = {}
    
    def addUriWithData(self, uris: list[str], data: Any) -> str:
        gid = self.addUri(uris)
        self.gidCardNameMap[gid] = data
        return gid
    
    def getData(self, gid: str) -> Any:
        return self.gidCardNameMap[gid]
