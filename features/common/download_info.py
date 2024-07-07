from typing import Optional


class DownloadInfo:
    """
    下载任务

    实例化后需要loadFromAria2RawData，否则是默认值。
    """

    ARIA2_RPC_KEYS = [
        "status",
        "totalLength",
        "completedLength",
        "downloadSpeed",
        "errorCode",
        "errorMessage",
        "files",
    ]

    def __init__(self) -> None:
        self.status: str = ""
        self.totalLength = 0
        self.completedLength = 0
        self.downloadSpeed = 0
        # 只有已停止/已完成的下载才有error信息
        self.errorCode: Optional[str] = None
        self.errorMessage: Optional[str] = None

    def loadFromAria2RawData(self, result: dict) -> None:
        self.status = result["status"]
        self.totalLength = int(result["totalLength"])
        self.completedLength = int(result["completedLength"])
        self.downloadSpeed = int(result["downloadSpeed"])
        self.fileRelativePath = result["files"][0]["path"]
        # 只有已停止/已完成的下载才有error信息
        self.errorCode = result.get("errorCode", None)
        self.errorMessage = result.get("errorMessage", None)
