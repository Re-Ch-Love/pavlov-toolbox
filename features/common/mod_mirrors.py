import json
from PySide6.QtWidgets import QApplication

from features.common.qrequest import QPromise, QRequestReady


FROST_BLADE_MIRROR_MANIFEST_URL = "https://api.pavlov-toolbox.rech.asia/mod-download-mirrors/FrostBlade"

def getDownloadUrlFromFrostBladeMirror(rid: int) -> QPromise:
    """"""
    def extractDownloadUrl(responseContent: bytes) -> str | None:
        manifestObj: dict = json.loads(responseContent)
        result = next((item for item in manifestObj.values() if item["id"] == rid), None)
        if (
            result is None
            or "windows" not in result
            or result["windows"] is None
            or "binary_url" not in result["windows"]
        ):
            return None
        return result["windows"]["binary_url"]
    return Globals.qRequestReady.get(FROST_BLADE_MIRROR_MANIFEST_URL).then(extractDownloadUrl)


if __name__ == "__main__":
    Globals = __import__("features.common.global_objects.Globals")
    app = Globals.createQApp()
    result = getDownloadUrlFromFrostBladeMirror(3467755)
    result.then(lambda res: print(res)).done()
    app.exec()
