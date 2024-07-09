from features.common.mod_installation import ModInstallationManager

# 全局单例对象
# 不放在一个class中的话，vscode里无法自动导入
class Globals:
    modInstallationManager = ModInstallationManager()