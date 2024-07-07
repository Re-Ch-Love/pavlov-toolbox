import os
import zipfile

from features.common.mod import ModData
from features.common.mod_installation import getModInstallationDir

import shutil
import app_config


def importMod(zipFilePath: str, modData: ModData):
    """导入Mod

    分为解压、补全、移动文件夹三个步骤"""
    # 定义该Mod解压补全时的临时目录路径
    tempDir = os.path.join(
        app_config.IMPORT_MOD_TEMP_DIR, f"UGC{modData.getResourceId()}"
    )
    _unzipModData(tempDir, zipFilePath)
    _writeTaintFile(tempDir, str(modData.getModFileLive("windows")))
    _moveModTempDirToInstallationDir(tempDir)


def _unzipModData(outputDir: str, zipFilePath: str):
    # 如果输出目录存在，则清空
    if os.path.exists(outputDir):
        shutil.rmtree(outputDir)
    else:
        os.makedirs(outputDir)
    outputDir = os.path.join(outputDir, "Data")
    # 使用zipfile模块解压ZIP文件到目标目录
    with zipfile.ZipFile(zipFilePath, "r") as zip_file:
        zip_file.extractall(outputDir)


def _writeTaintFile(outputDir: str, content: str):
    taintFilePath = os.path.join(outputDir, "taint")
    with open(taintFilePath, "w", encoding="utf-8") as file:
        file.write(content)


def _moveModTempDirToInstallationDir(sourceDir: str):
    r"""将Mod从临时目录移动到安装目录"""
    modInstallationDir = getModInstallationDir()
    # 判断安装目录是否存在，如果不存在则新建
    if not os.path.exists(modInstallationDir):
        os.makedirs(modInstallationDir)
    # 获取源目录最后一段（即目录名称）
    modDirName = os.path.basename(sourceDir)
    targetDir = os.path.join(modInstallationDir, modDirName)
    # 如果目录存在，使用shutil递归删除目录
    if os.path.exists(targetDir):
        shutil.rmtree(targetDir)
    # 使用shutil移动目录
    shutil.move(sourceDir, targetDir)

if __name__ == "__main__":
    importMod(".\\downloads\\modfile_2802847.129.zip", ModData.constructFromServer(2802847))