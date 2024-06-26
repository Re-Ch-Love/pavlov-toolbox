from typing import Dict, List
import requests
import urllib.parse
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import QThread, Slot, Signal, Qt
from ui.common import exec_simple_dialog
from ui.search_ui import Ui_search
from features.common import *


SEARCH_LIMIT = 10


class SearchThread(QThread):
    onFinish = Signal(list)
    onFatal = Signal(str)
    onNotFound = Signal()

    def __init__(self, input: str):
        super().__init__()
        self.input = input

    def run(self):
        res = requests.get(
            f"https://pavlov.rech.asia/modio/v1/games/@pavlov/mods?_limit={SEARCH_LIMIT}&_offset=0&_sort=-popular&_q={urllib.parse.quote(self.input)}",
        )
        if res.status_code != 200:
            raise AppInternalException(f"res.status_code != 200 (_q={self.input})")
        data: List[Dict] = res.json()["data"]
        if len(data) == 0:
            self.onNotFound.emit()
            return
        result_table = []
        for mod in data:
            name = mod["name"]
            rid = str(mod["id"])
            # print(name, rid)
            no_dl_url_flag = False
            try:
                # mod = get_mod_json(rid)
                taint = get_mod_platform_id(mod, "windows")
            except AppInternalException as e:
                # self.onFatal.emit(str(e))
                no_dl_url_flag = True
            except requests.exceptions.ConnectionError as e:
                self.onFatal.emit(str(e))
                return
            if no_dl_url_flag:
                dl_url = "无法获取"
            else:
                dl_url = join_mod_download_url(mod, taint)
            # print(dl_url)
            result_table.append({"name": name, "rid": rid, "dl_url": dl_url})
        self.onFinish.emit(result_table)


class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_search()
        self.ui.setupUi(self)
        self.ui.pbtn_search.clicked.connect(self.search)
        self.is_searching = False
        header = self.ui.table_result.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

    def search(self):
        if self.is_searching:
            return
        self.is_searching = True
        input = self.ui.lnedit_input.text()

        @Slot(str)
        def onFatal(reason: str):
            self.is_searching = False
            self.search_thread.quit()
            exec_simple_dialog("错误", f"无法获取搜索结果。\n详细信息：{reason}")

        def onNotFound():
            exec_simple_dialog("搜索完毕", "没有找到相关的Mod。")

        @Slot(list)
        def onFinish(table: List[Dict[str, str]]):
            # print(table)
            self.ui.table_result.setRowCount(len(table))
            def notEditableiItem(context: str):
                item = QTableWidgetItem(context)
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                return item
            for index, data in enumerate(table):
                self.ui.table_result.setItem(index, 0, notEditableiItem(data["name"]))
                self.ui.table_result.setItem(index, 1, notEditableiItem(data["rid"]))
                self.ui.table_result.setItem(index, 2, notEditableiItem(data["dl_url"]))

        def onThreadFinished():
            self.is_searching = False
            self.search_thread.deleteLater()

        self.search_thread = SearchThread(input)
        self.search_thread.onFatal.connect(onFatal)
        self.search_thread.onFinish.connect(onFinish)
        self.search_thread.onNotFound.connect(onNotFound)
        self.search_thread.finished.connect(onThreadFinished)
        self.search_thread.start()
