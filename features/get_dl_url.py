from typing import List
import requests
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Slot, Signal, QThread
from features.common import AppInternalException
from ui.get_mod_dl_url_ui import Ui_getModDlUrl
from ui.common import exec_simple_dialog
from features.common import *

# In this file, mod_id == rid (Resource ID)


MOD_LIST_URL = "https://pavlov.rech.asia/mod-list?version=%s&name=%s"
MOD_LIST_MAP_URL = "https://pavlov.rech.asia/mod-list-map"


def get_mod_list_map():
    res = requests.get(MOD_LIST_MAP_URL)
    if res.status_code != 200:
        raise AppInternalException("get_mod_list_from_remote: status_code != 200")
    return res.json()


def get_rid_list_from_remote(version: str, name: str) -> List[str]:
    res = requests.get(MOD_LIST_URL % (version, name))
    if res.status_code != 200:
        raise AppInternalException("get_mod_list_from_remote: status_code != 200")
    return res.json()["default"]


class ConvertThread(QThread):
    onFinish = Signal(str)
    onError = Signal(str)
    onFatal = Signal(str)

    def __init__(self, rid_list):
        super().__init__()
        self.rid_list = rid_list

    def run(self):
        for rid in self.rid_list:
            try:
                mod = get_mod_json(rid)
                taint = get_mod_platform_id(mod, "windows")
            except AppInternalException as e:
                self.onError.emit(rid)
                continue
            except requests.exceptions.ConnectionError as e:
                self.onFatal.emit(str(e))
                return
            download_url = join_mod_download_url(mod, taint)
            self.onFinish.emit(download_url)


class GetModListMapThread(QThread):
    onFatal = Signal(str)
    onFinish = Signal(dict)

    def run(self):
        try:
            data = get_mod_list_map()
        except AppInternalException as e:
            self.onFatal.emit(str(e))
        self.onFinish.emit(data)

class GetDlUrlWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_getModDlUrl()
        self.ui.setupUi(self)
        self.ui.ptedit_resourceId.setPlaceholderText(
            "请填写或点击上方一键填充资源ID\n示例：\n2771448\n2771449\n2771450"
        )
        self.ui.pbtn_convert.clicked.connect(self.convert)
        self.ui.pbtn_replace.clicked.connect(self.replace)
        self.ui.pbtn_copy.clicked.connect(self.copy)
        self.mod_list_map: Dict[str, str] = {}
        self.is_converting = False
        self.start_load_mod_list_thread()
    
    def start_load_mod_list_thread(self):
        self.get_mod_list_map_thread = GetModListMapThread()
        self.get_mod_list_map_thread.onFinish.connect(self.display_mod_list_map)
        self.get_mod_list_map_thread.onFatal.connect(self.get_mod_list_map_error)
        self.get_mod_list_map_thread.finished.connect(lambda: self.get_mod_list_map_thread.deleteLater)
        self.get_mod_list_map_thread.start()

    @Slot(str)
    def get_mod_list_map_error(self, reason: str):
        exec_simple_dialog("错误", f"无法获取mod列表一键填充相关数据，请检查网络连接。\n详细信息：{reason}")

    @Slot(dict)
    def display_mod_list_map(self, mod_list_map):
        self.mod_list_map = mod_list_map
        self.ui.cbbox_modListName.addItems(list(self.mod_list_map.keys()))
        

    def copy(self):
        self.ui.ptedit_dlUrl.selectAll()
        self.ui.ptedit_dlUrl.copy()

    def convert(self):
        if self.is_converting:
            return
        self.is_converting = True
        rid_list = []
        error_list = []
        # 检查
        for rid in self.ui.ptedit_resourceId.toPlainText().split("\n"):
            rid = rid.strip()
            if rid == "":
                continue
            if not rid.isdigit():
                error_list.append(rid)
            rid_list.append(rid)
        if len(error_list) != 0:
            context = "以下资源ID不符合要求，应为纯数字：\n" + ",\n".join(error_list)
            exec_simple_dialog("错误", context)
            self.is_converting = False
            return
        # 清空原有的
        self.ui.ptedit_dlUrl.setPlainText("")
        # 转换
        error_list = []

        @Slot(str)
        def onError(rid):
            error_list.append(rid)

        @Slot(str)
        def onFinish(dl_url):
            self.ui.ptedit_dlUrl.appendPlainText(dl_url)

        @Slot(str)
        def onFatal(reason):
            self.is_converting = False
            self.convert_thread.quit()
            exec_simple_dialog(
                "错误", f"发送api请求时发生连接错误。\n详细信息：{reason}"
            )

        def onThreadFinish():
            if len(error_list) != 0:
                context = "以下资源ID无法获取下载链接：\n" + "\n".join(error_list)
                exec_simple_dialog("错误", context)
            else:
                exec_simple_dialog("转换完成", "全部转换成功！")
            self.is_converting = False
            self.convert_thread.deleteLater()

        self.convert_thread = ConvertThread(rid_list)
        self.convert_thread.onError.connect(onError)
        self.convert_thread.onFinish.connect(onFinish)
        self.convert_thread.onFatal.connect(onFatal)
        self.convert_thread.finished.connect(onThreadFinish)
        self.convert_thread.start()

    def replace(self):
        name = self.mod_list_map[self.ui.cbbox_modListName.currentText()]
        try:
            rid_list = get_rid_list_from_remote("latest", name)
        except requests.exceptions.ConnectionError as e:
            exec_simple_dialog("错误", f"发送api请求时发生连接错误。\n详细信息：{e}")
            return
        self.ui.ptedit_resourceId.setPlainText("\n".join(rid_list))
