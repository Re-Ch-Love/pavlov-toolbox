from common.mod.installation.extra_info import ModInstallationInfo


class ModDownloadTaskInfo:
    ARIA2_RPC_KEYS = [
        "gid",
        "status",
        "totalLength",
        "completedLength",
        "downloadSpeed",
        "errorCode",
        "errorMessage",
        "files",
    ]

    def __init__(self, data: dict, info: ModInstallationInfo) -> None:
        self._data = data
        self._installationInfo: ModInstallationInfo = info

    @property
    def installationInfo(self) -> ModInstallationInfo:
        return self._installationInfo

    @property
    def gid(self) -> str:
        return str(self._data["gid"])

    @property
    def status(self) -> str:
        return str(self._data["status"])

    @property
    def totalLength(self):
        return int(self._data["totalLength"])

    @property
    def completedLength(self):
        return int(self._data["completedLength"])

    @property
    def downloadSpeed(self):
        return int(self._data["downloadSpeed"])

    @property
    def fileRelativePath(self):
        return str(self._data["files"][0]["path"])

    @property
    def errorCode(self):
        return str(self._data.get("errorCode", None))

    @property
    def errorMessage(self):
        return str(self._data.get("errorMessage", None))
