# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'server_interface.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QSizePolicy,
    QTableWidgetItem, QVBoxLayout, QWidget)

from qfluentwidgets import (ComboBox, PrimaryPushButton, TableWidget)

class Ui_ServerModInterface(object):
    def setupUi(self, ServerModInterface):
        if not ServerModInterface.objectName():
            ServerModInterface.setObjectName(u"ServerModInterface")
        ServerModInterface.resize(785, 482)
        self.verticalLayout_2 = QVBoxLayout(ServerModInterface)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.serverComboBox = ComboBox(ServerModInterface)
        self.serverComboBox.setObjectName(u"serverComboBox")

        self.horizontalLayout.addWidget(self.serverComboBox)

        self.installButton = PrimaryPushButton(ServerModInterface)
        self.installButton.setObjectName(u"installButton")

        self.horizontalLayout.addWidget(self.installButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tableWidget = TableWidget(ServerModInterface)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.tableWidget)


        self.retranslateUi(ServerModInterface)

        QMetaObject.connectSlotsByName(ServerModInterface)
    # setupUi

    def retranslateUi(self, ServerModInterface):
        ServerModInterface.setWindowTitle(QCoreApplication.translate("ServerModInterface", u"Form", None))
        self.serverComboBox.setText(QCoreApplication.translate("ServerModInterface", u"PushButton", None))
        self.installButton.setText(QCoreApplication.translate("ServerModInterface", u"\u4e00\u952e\u5b89\u88c5", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ServerModInterface", u"\u8d44\u6e90ID", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ServerModInterface", u"\u540d\u79f0", None));
    # retranslateUi

