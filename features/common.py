from typing import Dict, List
import requests



class AppInternalException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
def get_mod_json(mod_id: str) -> dict:
    res = requests.get(
        f"https://pavlov.rech.asia/modio/v1/games/@pavlov/mods?_limit=1&_offset=0&_sort=-popular&id={mod_id}",
    )
    if res.status_code != 200:
        raise AppInternalException(f"res.status_code != 200 (modId={mod_id})")
    data = res.json()["data"]
    if len(data) == 0:
        raise AppInternalException(f"len(data) == 0 (modId={mod_id})")
    return data[0]


def get_mod_platform_id(mod: dict, platform_name: str) -> str:
    platform_list: List[Dict] = mod["platforms"]
    for platform in platform_list:
        if platform["platform"] == platform_name:
            return str(platform["modfile_live"])
    raise AppInternalException(f"platform `{platform_name}` not found")


def join_mod_download_url(mod: dict, platform_id: str) -> str:
    return f"https://g-3959.modapi.io/v1/games/3959/mods/{mod['id']}/files/{platform_id}/download"