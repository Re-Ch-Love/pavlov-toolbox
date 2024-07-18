### 项目结构

```
/
|-- aria2  aria2的可执行文件和 Python RPC 客户端
|-- common  一些通用的模块，通常与 Qt 无关或低耦合
|   |-- mod  Mod 相关的模块
|-- interfaces  App界面相关
|-- ui_design  在 Qt Designer 中设计的 UI 和由 pyside6-uic 编译 UI 文件，不作任何手动修改
|-- dev_docs  开发文档
|   |-- README.md
|-- requirements.txt  该项目使用的依赖库及其版本
|-- build.ps1  构建脚本
|-- README.md
```

### 注意事项
你可能需要运行下面的命令来转换代码风格
```
pyside6-genpyi all --feature snake_case true_property
```