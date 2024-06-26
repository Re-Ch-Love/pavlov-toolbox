# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_search(object):
    def setupUi(self, search):
        if not search.objectName():
            search.setObjectName(u"search")
        search.resize(800, 547)
        self.verticalLayout = QVBoxLayout(search)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lnedit_input = QLineEdit(search)
        self.lnedit_input.setObjectName(u"lnedit_input")

        self.horizontalLayout.addWidget(self.lnedit_input)

        self.pbtn_search = QPushButton(search)
        self.pbtn_search.setObjectName(u"pbtn_search")

        self.horizontalLayout.addWidget(self.pbtn_search)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label = QLabel(search)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.table_result = QTableWidget(search)
        if (self.table_result.columnCount() < 3):
            self.table_result.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_result.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_result.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_result.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table_result.setObjectName(u"table_result")
        self.table_result.horizontalHeader().setVisible(True)
        self.table_result.horizontalHeader().setStretchLastSection(False)
        self.table_result.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.table_result)


        self.retranslateUi(search)

        QMetaObject.connectSlotsByName(search)
    # setupUi

    def retranslateUi(self, search):
        search.setWindowTitle(QCoreApplication.translate("search", u"Form", None))
        self.lnedit_input.setPlaceholderText(QCoreApplication.translate("search", u"\u8bf7\u8f93\u5165Mod\u540d\u79f0", None))
        self.pbtn_search.setText(QCoreApplication.translate("search", u"\u641c\u7d22", None))
        self.label.setText(QCoreApplication.translate("search", u"<html><head/><body><p><span style=\" font-weight:700;\">\u9009\u4e2d\u5355\u5143\u683c\u540e\u6309\u4e0b Ctrl+C \u5373\u53ef\u590d\u5236</span></p></body></html>", None))
        ___qtablewidgetitem = self.table_result.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("search", u"\u540d\u79f0", None));
        ___qtablewidgetitem1 = self.table_result.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("search", u"\u8d44\u6e90ID", None));
        ___qtablewidgetitem2 = self.table_result.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("search", u"\u4e0b\u8f7d\u5730\u5740", None));
    # retranslateUi

