class DownloadJob:
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
        "files"
    ]

    def __init__(self) -> None:
        # self.displayName = None
        # self.hintName = None
        self.status: str = ""
        self.totalLength = 0
        self.completedLength = 0
        self.downloadSpeed = 0
        # 只有已停止/已完成的下载才有error信息
        self.errorCode: str | None = None
        self.errorMessage: str | None = None

    def loadFromAria2RawData(self, result: dict) -> None:
        # self.displayName = displayName
        # self.hintName = hintName
        self.status: str = result["status"]
        self.totalLength = int(result["totalLength"])
        self.completedLength = int(result["completedLength"])
        self.downloadSpeed = int(result["downloadSpeed"])
        # 只有已停止/已完成的下载才有error信息
        self.errorCode: str | None = result.get("errorCode", None)
        self.errorMessage: str | None = result.get("errorMessage", None)

    # def getDiff(self, other: "Aria2DownloadJob") -> "Aria2DownloadJobDiff":
    #     """
    #     返回两个Job的差异，用于在UI中更新不一样的内容

    #     一样的内容会被置为None，不一样的内容会保留other中的。
    #     """
    #     status = None if self.status == other.status else other.status
    #     totalLength = (
    #         None if self.totalLength == other.totalLength else other.totalLength
    #     )
    #     completedLength = (
    #         None
    #         if self.completedLength == other.completedLength
    #         else other.completedLength
    #     )
    #     downloadSpeed = (
    #         None if self.downloadSpeed == other.downloadSpeed else other.downloadSpeed
    #     )
    #     errorCode = None if self.errorCode == other.errorCode else other.errorCode
    #     errorMessage = (
    #         None if self.errorMessage == other.errorMessage else other.errorMessage
    #     )
    #     return Aria2DownloadJobDiff(
    #         status, totalLength, completedLength, downloadSpeed, errorCode, errorMessage
    #     )

    # def update(self, other: "Aria2DownloadJobDiff"):
    #     if other.status:
    #         self.status = other.status
    #     if other.totalLength:
    #         self.totalLength = other.totalLength
    #     if other.completedLength:
    #         self.completedLength = other.completedLength
    #     if other.downloadSpeed:
    #         self.downloadSpeed = other.downloadSpeed
    #     if other.errorCode:
    #         self.errorCode = other.errorCode
    #     if other.errorMessage:
    #         self.errorMessage = other.errorMessage


# class Aria2DownloadJobDiff:
#     def __init__(
#         self,
#         status: str | None = None,
#         totalLength: int | None = None,
#         completedLength: int | None = None,
#         downloadSpeed: int | None = None,
#         errorCode: str | None = None,
#         errorMessage: str | None = None,
#     ) -> None:
#         self.status = status
#         self.totalLength = totalLength
#         self.completedLength = completedLength
#         self.downloadSpeed = downloadSpeed
#         # 只有已停止/已完成的下载才有error信息
#         self.errorCode = errorCode
#         self.errorMessage = errorMessage
