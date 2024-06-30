from typing import Callable, Dict, List, Tuple

import requests


class Aria2ConfigException(Exception):
    pass


class Aria2ConfigManager:
    """
    Aria2的配置文件管理器

    new之后，先load()，然后可以修改其中的config属性。
    最后使用dump()保存

    注意：该类无法读取和写入注释
    """

    def __init__(self, configPath: str):
        self.configPath = configPath
        self.config: Dict[str, str] = {}

    def load(self):
        with open(self.configPath, "r") as file:
            for line in file:
                if "=" not in line:
                    raise Aria2ConfigException()
                key, value = line.strip().split("=", 1)
                self.config[key] = value

    def dump(self):
        with open(self.configPath, "w") as file:
            for key, value in self.config.items():
                file.write(f"{key}={value}\n")

    def updateTrackers(self) -> int:
        """
        更新trackers

        会尝试从不同的tracker中获取，返回成功获取到的的trakcer list的数量。如果是0说明更新失败
        """
        # tracker list 处理器，元组中第一个是 tracker list 获取地址，第二个是处理函数（要处理成a:b:c:d）的形式
        trackerListHandlers: List[Tuple[str, Callable[[str], str]]] = [
            ("https://cf.trackerslist.com/all_aria2.txt", lambda text: text),
            (
                "https://ngosang.github.io/trackerslist/trackers_all_ip.txt",
                lambda text: ",".join(
                    [line for line in text.split("\n") if line.strip() != ""]
                ),
            ),
        ]
        successCount = 0
        trackers = ""
        for url, handler in trackerListHandlers:
            try:
                res = requests.get(url)
                if trackers == "":
                    trackers = handler(res.content.decode())
                else:
                    trackers += "," + handler(res.content.decode())
                successCount += 1
            except requests.exceptions.ConnectionError:
                continue
        if successCount != 0 and trackers != "":
            self.config["bt-tracker"] = trackers
        return successCount


# aria2.conf
# ------
# dir=downloads
# continue=true
# enable-rpc=true
# max-connection-per-server=5
# rpc-secret=p-%5{=O+):Pc7QqP
# bt-tracker=udp://93.158.213.92:1337/announce,http://93.158.213.92:1337/announce,udp://66.160.128.46:1337/announce,udp://185.243.218.213:80/announce,udp://89.234.156.205:451/announce,udp://208.83.20.20:6969/announce,udp://23.153.248.83:6969/announce,udp://45.9.60.30:6969/announce,udp://167.99.185.219:6969/announce,udp://125.227.79.123:80/announce,udp://135.125.202.143:6969/announce,udp://83.146.118.175:6969/announce,udp://211.23.142.127:6969/announce,udp://82.156.24.219:6969/announce,udp://15.204.56.171:6969/announce,udp://83.102.180.21:80/announce,udp://104.244.77.87:6969/announce,udp://37.27.4.53:6969/announce,udp://94.243.222.100:6969/announce,udp://51.68.174.87:6969/announce,udp://207.241.231.226:6969/announce,udp://207.241.226.111:6969/announce,udp://51.159.54.68:6666/announce,http://211.23.142.127:6969/announce,udp://83.31.215.217:6969/announce,udp://51.222.82.36:6969/announce,udp://193.42.111.57:9337/announce,udp://181.214.58.63:6969/announce,udp://5.255.124.190:6969/announce,udp://52.58.128.163:6969/announce,udp://85.239.33.28:6969/announce,udp://15.204.57.168:6969/announce,udp://35.227.59.57:6969/announce,udp://176.31.250.174:6969/announce,udp://37.235.176.37:2710/announce,udp://51.15.41.46:6969/announce,udp://107.175.221.194:6969/announce,udp://185.230.4.150:1337/announce,udp://88.216.2.71:6969/announce,udp://179.43.155.30:6969/announce,udp://62.210.114.129:6969/announce,udp://34.89.51.235:6969/announce,udp://178.32.222.98:3391/announce,udp://23.163.56.66:6969/announce,udp://176.99.7.59:6969/announce,udp://62.138.18.152:6969/announce,udp://104.244.77.14:1337/announce,udp://5.102.159.190:6969/announce,http://83.31.215.217:6969/announce,http://125.227.79.123:80/announce,http://181.214.58.63:6969/announce,http://95.217.167.10:6969/announce,http://34.89.51.235:80/announce,http://159.148.57.222:6969/announce,http://15.204.57.168:6969/announce,http://5.182.86.242:6969/announce,http://104.244.77.14:1337/announce,udp://130.61.158.165:6969/announce,udp://91.238.104.240:6969/announce,udp://143.198.64.177:6969/announce,udp://64.23.195.62:6969/announce,udp://89.47.160.50:6969/announce,udp://138.124.183.78:6969/announce,udp://209.126.11.233:6969/announce,udp://176.123.1.180:6969/announce,udp://198.12.89.149:6969/announce,udp://45.135.134.94:6969/announce,udp://185.216.179.62:25/announce,udp://121.199.16.229:6969/announce,udp://116.202.49.58:6969/announce,udp://37.59.48.81:6969/announce,udp://96.126.98.54:6969/announce,udp://51.15.26.25:6969/announce,http://184.61.17.58:9000/announce,http://194.87.70.68:2710/announce,http://154.29.150.159:17715/announce,http://46.231.241.43:6969/announce
# ------

if __name__ == "__main__":
    configManager = Aria2ConfigManager("aria2\\aria2.conf")
    configManager.load()
    # configManager.config.pop("test")
    successCount = configManager.updateTrackers()
    print("success", successCount)
    configManager.dump()
