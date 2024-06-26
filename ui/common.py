from typing import Any, Callable, Optional
from PySide6.QtWidgets import QDialog,  QLabel, QPushButton, QVBoxLayout

def exec_simple_dialog(title: str, context: str, pbtnText="确定", onPbtnClick: Optional[Callable[[], Any]] = None):
    dialog = QDialog()
    dialog.setWindowTitle(title)
    # dialog.setGeometry(QRect)
    layout = QVBoxLayout()
    layout.addWidget(QLabel(context))
    pbtn = QPushButton(text=pbtnText)
    def onClick():
        if onPbtnClick is not None:
            onPbtnClick()
        dialog.done(0)
    pbtn.clicked.connect(onClick)
    layout.addWidget(pbtn)
    dialog.setLayout(layout)
    dialog.exec()