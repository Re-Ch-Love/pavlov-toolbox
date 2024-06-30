from PySide6.QtWidgets import QWidget

from ui.home_interface_ui import Ui_HomeInterface


class HomeInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_HomeInterface()
        self.ui.setupUi(self)