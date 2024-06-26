# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'unzip_and_complete.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_unzipAndComplete(object):
    def setupUi(self, unzipAndComplete):
        if not unzipAndComplete.objectName():
            unzipAndComplete.setObjectName(u"unzipAndComplete")
        unzipAndComplete.resize(800, 547)
        self.horizontalLayout = QHBoxLayout(unzipAndComplete)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pbtn_selectFiles = QPushButton(unzipAndComplete)
        self.pbtn_selectFiles.setObjectName(u"pbtn_selectFiles")

        self.verticalLayout.addWidget(self.pbtn_selectFiles)

        self.label_2 = QLabel(unzipAndComplete)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.list_selectedFiles = QListWidget(unzipAndComplete)
        self.list_selectedFiles.setObjectName(u"list_selectedFiles")

        self.verticalLayout.addWidget(self.list_selectedFiles)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pbtn_unzipAndComplete = QPushButton(unzipAndComplete)
        self.pbtn_unzipAndComplete.setObjectName(u"pbtn_unzipAndComplete")

        self.verticalLayout_2.addWidget(self.pbtn_unzipAndComplete)

        self.label = QLabel(unzipAndComplete)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label)

        self.tedit_output = QTextEdit(unzipAndComplete)
        self.tedit_output.setObjectName(u"tedit_output")

        self.verticalLayout_2.addWidget(self.tedit_output)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(unzipAndComplete)

        QMetaObject.connectSlotsByName(unzipAndComplete)
    # setupUi

    def retranslateUi(self, unzipAndComplete):
        unzipAndComplete.setWindowTitle(QCoreApplication.translate("unzipAndComplete", u"Form", None))
        self.pbtn_selectFiles.setText(QCoreApplication.translate("unzipAndComplete", u"\u9009\u62e9Mod\u538b\u7f29\u5305", None))
        self.label_2.setText(QCoreApplication.translate("unzipAndComplete", u"\u5df2\u9009\u62e9\u7684\u6587\u4ef6", None))
        self.pbtn_unzipAndComplete.setText(QCoreApplication.translate("unzipAndComplete", u"\u89e3\u538b\u5e76\u8865\u5168", None))
        self.label.setText(QCoreApplication.translate("unzipAndComplete", u"\u8f93\u51fa\u4fe1\u606f", None))
        self.tedit_output.setPlaceholderText("")
    # retranslateUi

