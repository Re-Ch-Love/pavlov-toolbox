from PySide6.QtWidgets import QApplication
import aiohttp
import requests


FROST_BLATE_MIRROR_MANIFEST_URL = (
    "https://api.pavlov-toolbox.rech.asia/mod-download-mirrors/FrostBlade"
)


def getFrostBladeMirrorUrl(rid: int) -> str | None:
    response = requests.get(FROST_BLATE_MIRROR_MANIFEST_URL)
    if response.status_code != 200:
        return None
    manifestObj: dict = response.json()
    result = next((item for item in manifestObj.values() if item["id"] == rid), None)
    if (
        result is None
        or "windows" not in result
        or result["windows"] is None
        or "binary_url" not in result["windows"]
    ):
        return None
    return result["windows"]["binary_url"]

if __name__ == "__main__":
    app = QApplication()

