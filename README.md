# Pavlov工具箱

## 项目架构

主要目录和文件

|        名称        | 解释                                                                         |
| :----------------: | ---------------------------------------------------------------------------- |
|      `aria2/`      | aria2的可执行文件和 Python RPC 客户端                                        |
|    `features/`     | App功能相关逻辑和功能最终的控件                                              |
|       `ui/`        | 在 Qt Designer 中设计的 UI 和由 pyside6-uic 编译 UI 文件，不作任何手动修改。 |
|    `build.ps1`     | 构建脚本                                                                     |
| `requirements.txt` | 该项目使用的依赖库及其版本                                                   |

## 构建

安装完 `requirements.txt` 中的依赖后，运行 `build.ps1` 即可。

## 鸣谢

本项目使用了以下第三方软件/包，特此感谢以下软件/包的贡献者。

- 内置的下载器 [aria2](https://github.com/aria2/aria2)
- 打包工具 PyInstaller
- 图形界面框架 Qt 与其绑定库 PySide6