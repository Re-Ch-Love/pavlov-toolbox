from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem
from qfluentwidgets import MessageBox


class ChineseMessageBox(MessageBox):
    def __init__(self, title: str, content: str, parent):
        super().__init__(title, content, parent)
        self.yesButton.setText("确定")
        self.cancelButton.setText("取消")


# 大写开头是因为该函数模拟了一个继承的行为，所以将它当作一个类来看待
def UneditableQTableWidgetItem(content: str):
    item = QTableWidgetItem(content)
    item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
    return item