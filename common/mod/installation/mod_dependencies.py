import json
from typing import List
from PySide6.QtWidgets import QApplication
from qfluentwidgets import QObject

from common.mod.mod_data import MOD_BATCH_REQUEST_URL, ModData
from common.qrequest import QDataPromise, QPromise, QRequestReady


DEPENDENCIES_URL = (
    "https://api.pavlov-toolbox.rech.asia/modio/v1/games/3959/mods/%d/dependencies?recursive=true"
)


def getModDependencies(parent: QObject, rid: int) -> QPromise:
    def getDependencies(content: bytes) -> List[int]:
        jsonObj = json.loads(content)
        if jsonObj["result_total"] == 0:
            return []
        else:
            data = jsonObj["data"]
            # 因为获取依赖Mod时返回的数据格式，与获取Mod的不一样，所以这里需要用rid再请求一次
            return [item["mod_id"] for item in data]

    def dependenciesToModData(rids: List[int] | None) -> QPromise:
        nonlocal parent
        if not rids:
            return QDataPromise([])
        else:
            ridsParam = ",".join([str(rid) for rid in rids])
            return (
                QRequestReady(parent)
                .get(MOD_BATCH_REQUEST_URL % ridsParam)
                .then(lambda content: [ModData(item) for item in json.loads(content)["data"]])
            )

    return (
        QRequestReady(parent)
        .get(DEPENDENCIES_URL % rid)
        .then(getDependencies)
        .then(dependenciesToModData)
    )


if __name__ == "__main__":
    app = QApplication()
    modList = [
        3061028,
        3048982,
        3116594,
        3094680,
        3243988,
        3002600,
        3020535,
        3002208,
        2996823,
        3051820,
        2804502,
        2879562,
        2867687,
        # 2871454,
        # 3265534,
        # 2856317,
        # 3467755,
        # 3924157,
        # 3975268,
        # 3268798,
        # 3943563,
        # 3969882,
        # 3901501,
    ]

    # def onFinish(modData: ModData, dependencies: List[ModData]):
    #     print(modData.resourceId, dependencies)

    # def onError(modData: ModData, reason: str):
    #     print(modData.resourceId, f"error: {reason}")

    # for rid in modList:
    #     ModDependenciesProcessor(
    #         ModData.constructFromServer(rid), onFinish, onError, app
    #     )

    # 3243988 有依赖
    (getModDependencies(app, 3243988).then(lambda modDataList: print(modDataList)).done())
    app.exec()
