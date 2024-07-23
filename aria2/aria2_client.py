import json
import os
import secrets
import subprocess
import sys
import time
from typing import Any, List, Optional
import requests
import app_config
from common.log import AppLogger
from common.path import getResourcePath


class Aria2RpcException(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = str(code)  # 防止传入int类型的code
        self.message = message

    def __str__(self):
        return "{code: %s, message: %s}" % (self.code, self.message)


class Aria2Client:
    """Aria2客户端，通过requests库与Aria2进行JsonRPC通信。

    实例化该类后自动启动Aria2子进程，该类被析构时会自动**尝试结束**aria2子进程。

    参考[Aria2非官方中文文档](https://aria2.document.top/zh/aria2c.html#id42)
    """

    def __init__(self):
        self.rpcUrl = "http://127.0.0.1:6800/jsonrpc"
        self.rpcHeaders = {"Content-Type": "application/json"}
        self.rpcId: int = 0

        executablePath = getResourcePath(os.path.join("aria2", "aria2c.exe"))
        configPath = getResourcePath(os.path.join("aria2", "aria2.conf"))
        self.rpcSecret = secrets.token_hex(32)
        command = f"{executablePath} --conf-path {configPath} --rpc-secret {self.rpcSecret} --dir {app_config.TEMP_DOWNLOAD_DIR}"
        command = command.split()

        self.process = subprocess.Popen(
            command,
            stdout=sys.stdout,
            stderr=sys.stderr,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

    def __del__(self):
        AppLogger().info("尝试结束 aria2 子进程")
        if self.process.poll() is None:  # 检查子进程是否还在运行
            self.process.terminate()

    def _request(self, method: str, *params: Any):
        """使用给定的params请求给定的method，可能会抛出`requests.exceptions.ConnectionError`"""
        self.rpcId += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self.rpcId,
            "method": method,
            "params": [f"token:{self.rpcSecret}"],
        }
        if params:
            payload["params"].extend(params)
        response = requests.post(self.rpcUrl, headers=self.rpcHeaders, data=json.dumps(payload))
        obj: dict = response.json()
        if "error" in obj.keys():
            raise Aria2RpcException(obj["error"]["code"], obj["error"]["message"])
        return obj

    def addUri(self, uris: List[str]) -> str:
        """添加下载任务，返回一个gid"""
        gid = self._request("aria2.addUri", uris)["result"]
        # self.gidList.append(gid)
        return gid

    def remove(self, gid: str):
        self._request("aria2.remove", gid)

    def pause(self, gid: str):
        self._request("aria2.pause", gid)

    def pauseAll(self):
        self._request("aria2.pauseAll")

    def unpause(self, gid: str):
        self._request("aria2.unpause", gid)

    def unpauseAll(self):
        self._request("aria2.unpauseAll")

    def tellStatus(self, gid: str, keys: Optional[list] = None):
        if keys:
            return self._request("aria2.tellStatus", gid, keys)
        else:
            return self._request("aria2.tellStatus", gid)

    def tellActive(self, keys: Optional[list] = None):
        if keys:
            return self._request("aria2.tellActive", keys)
        else:
            return self._request("aria2.tellActive")

    def tellWaiting(self, offset: int, num: int, keys: Optional[list] = None):
        if keys:
            return self._request("aria2.tellWaiting", offset, num, keys)
        else:
            return self._request("aria2.tellWaiting", offset, num)

    def tellStopped(self, offset: int, num: int, keys: Optional[list] = None):
        if keys:
            return self._request("aria2.tellStopped", offset, num, keys)
        else:
            return self._request("aria2.tellStopped", offset, num)

    def getGlobalStat(self):
        return self._request("aria2.getGlobalStat")

    def purgeDownloadResult(self):
        """此方法清除已完成/出错/已删除的下载以释放内存"""
        self._request("aria2.purgeDownloadResult")

    def removeDownloadResult(self, gid: str):
        """此方法从内存中删除由 gid 表示的已完成/出错/已删除的下载"""
        self._request("aria2.removeDownloadResult", gid)

    def getVersion(self) -> str:
        return self._request("aria2.getVersion")["result"]["version"]

    def shutdown(self):
        self._request("aria2.shutdown")

    def forceShutdown(self):
        self._request("aria2.forceShutdown")


if __name__ == "__main__":
    aria2 = Aria2Client()
    # aria2.startRpcServer()
    # time.sleep(1)
    gid = aria2.addUri(
        ["https://g-3959.modapi.io/v1/games/3959/mods/2804502/files/5245410/download"]
    )
    while True:
        print(aria2.tellActive())
        time.sleep(1)
