# 暂时不需要这个配置文件了

# import os
# import sys
# from typing import Any

# import toml


# # 配置文件存放路径
# # 一般为C:\Users\用户名\AppData\Roaming\PavlovToolbox\pavlovtoolbox-config.toml
# CONFIG_PATH = os.path.join(os.getenv("APPDATA", ""), "PavlovToolbox", "pavlovtoolbox-config.toml")


# class UserConfig:
#     def __init__(self) -> None:
#         # 如果文件不存在
#         if not os.path.exists(CONFIG_PATH):
#             # 递归创建目录（如果不存在）
#             os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
#             # 新建文件
#             with open(CONFIG_PATH, "w", encoding="utf-8") as f:
#                 toml.dump({}, f)
#             # 指定配置文件为空
#             self.config: dict[str, Any] = {}
#         else:
#             self.config: dict[str, Any] = toml.load(CONFIG_PATH)

#     @property
#     def logLevel(self) -> str:
#         return self.config.get("log_level", "INFO").upper()


# userConfig = UserConfig()
