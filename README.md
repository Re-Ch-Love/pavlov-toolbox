# Pavlov工具箱

## 简介

这是一个集多个实用功能为一体的 Pavlov（一款游戏） 工具箱。

其中包括（或计划包括）但不限于以下功能：

- [x] Mod 的搜索与安装
- [x] 特定服务器需要的 Mod 的安装
- [x] 本地 Mod 更新
- [x] 游戏知识库
- [ ] Mod 安装路径移动

## 已知问题

- [x] 页面切换时上面的信息不会刷新
- [ ] 安装任务过多时会发生bug

## 概览

[开发文档](./dev_docs/README.md)

## 构建

安装完 `requirements.txt` 中的依赖后，运行 `build.ps1` 即可。

## 鸣谢

本项目使用了以下第三方软件/包，特此感谢以下软件/包的贡献者。

- 内置的下载器 [aria2](https://github.com/aria2/aria2)
- 打包工具 PyInstaller
- 图形界面框架 Qt 与其绑定库 PySide6
