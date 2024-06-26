import os
from typing import Dict, List
import zipfile
import re
import re
from PySide6.QtWidgets import (
    QWidget,
    QFileDialog,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QTextEdit,
)
from PySide6.QtCore import QThread, Signal, Slot
from ui.unzip_and_complete_ui import Ui_unzipAndComplete

import requests
import shutil

OUTPUT_BASE_DIR = "output"

pattern = re.compile("^[a-zA-Z]+_?([0-9]+).*?\\.zip$")


def get_taint_content(mod_id: str) -> str:
    res = requests.get(
        f"https://pavlov.rech.asia/modio/v1/games/@pavlov/mods?_limit=1&_offset=0&_sort=-popular&id={mod_id}",
    )
    if res.status_code != 200:
        raise Exception(f"res.status_code != 200 (modId={mod_id})")
    mod = res.json()["data"][0]
    platform_list: List[Dict] = mod["platforms"]
    for platform in platform_list:
        if platform["platform"] == "windows":
            return str(platform["modfile_live"])
    raise Exception(f"platform windows not found")


def unzip_and_complete(file_path):
    filename = os.path.basename(file_path)
    match_result = pattern.match(filename)
    if match_result != None:
        mod_id = match_result.group(1)
        # 提取ZIP文件的名称（不含扩展名）
        zip_name = os.path.splitext(filename)[0]
        target_dir_name = f"UGC{mod_id}"
        # 构造目标目录的完整路径
        output_dir = os.path.join(OUTPUT_BASE_DIR, target_dir_name)
        output_data_dir = os.path.join(output_dir, "Data")
        taint_file_path = os.path.join(output_dir, "taint")
        # 如果目标目录存在，清空其中的内容
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        else:
            os.makedirs(output_dir)
        # 使用zipfile模块解压ZIP文件到目标目录
        with zipfile.ZipFile(file_path, "r") as zip_file:
            zip_file.extractall(output_data_dir)
        # 写入taint文件
        taint_content = get_taint_content(mod_id)
        with open(taint_file_path, "w", encoding="utf-8") as file:
            file.write(taint_content)


class UnzipAndCompleteThread(QThread):
    onStart = Signal(str)
    onFinish = Signal()
    onError = Signal(str)

    def __init__(self, file_path_list):
        super().__init__()
        self.file_path_list = file_path_list

    def run(self):
        for file_path in self.file_path_list:
            try:
                self.onStart.emit(file_path)
                unzip_and_complete(file_path)
                self.onFinish.emit()
            except Exception as e:
                self.onError.emit(str(e))

class UnzipAndCompleteWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_unzipAndComplete()
        self.ui.setupUi(self)
        self.ui.pbtn_selectFiles.clicked.connect(self.selectFiles)
        self.ui.pbtn_unzipAndComplete.clicked.connect(self.unzipAndComplete)
        self.file_path_list = []
        self.is_processing = False

    def selectFiles(self):
        dialog = QDialog()
        dialog.setWindowTitle("提示")
        layout = QVBoxLayout()
        layout.addWidget(
            QLabel(
                "按下 Ctrl+A 全选\n按住 Shift 并左键单击连选\n按住 Ctrl 并左键单击多选"
            )
        )
        pbtn = QPushButton(text="我知道了")

        def onClick():
            # nonlocal file_path_list
            self.file_path_list, _ = QFileDialog.getOpenFileNames(
                self, "选择Mod的压缩包", filter="*.zip"
            )
            dialog.done(0)

        pbtn.clicked.connect(onClick)
        layout.addWidget(pbtn)
        dialog.setLayout(layout)
        dialog.exec()
        filename_list = [
            os.path.basename(file_path) for file_path in self.file_path_list
        ]
        self.ui.list_selectedFiles.clear()
        self.ui.list_selectedFiles.addItems(filename_list)

    def unzipAndComplete(self):
        if self.is_processing:
            return
        self.is_processing = True

        output_manager = OutputManager(self.ui.tedit_output)
        count = 0
        success_count = 0

        @Slot(str)
        def onStart(file_path):
            nonlocal count
            count += 1
            output_manager.appendProcessing(file_path)

        def onFinish():
            nonlocal success_count
            success_count += 1
            output_manager.setSuccess()

        @Slot(str)
        def onError(reason):
            output_manager.setError(str(reason))

        def onThreadFinish():
            self.ui.tedit_output.append(
                f"全部处理完成，共计{count}个，成功{success_count}个，失败{count - success_count}个。"
            )
            self.is_processing = False
            self.process_thread.deleteLater()

        self.process_thread = UnzipAndCompleteThread(self.file_path_list)
        self.process_thread.onStart.connect(onStart)
        self.process_thread.onFinish.connect(onFinish)
        self.process_thread.onError.connect(onError)
        self.process_thread.finished.connect(onThreadFinish)
        self.process_thread.start()

class OutputManager:
    def __init__(self, textEdit: QTextEdit) -> None:
        self.textEdit = textEdit
        self.entries: List[str] = []
        self.current = ""

    def appendProcessing(self, current):
        self.entries.append(f"<p>正在处理{current}</p>")
        self.current = current
        self.update()

    def setSuccess(self):
        self.entries[len(self.entries) - 1] = (
            f"<p style='color: green;'>{self.current} 处理成功</p>"
        )
        self.update()

    def setError(self, reason: str):
        self.entries[len(self.entries) - 1] = (
            f"<p style='color: red;'>{self.current} 处理失败，原因：{reason}</p>"
        )
        self.update()

    def update(self):
        self.textEdit.setText("".join(self.entries))
