# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_interface.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import PushButton

class Ui_SettingsInterface(object):
    def setupUi(self, SettingsInterface):
        if not SettingsInterface.objectName():
            SettingsInterface.setObjectName(u"SettingsInterface")
        SettingsInterface.resize(770, 446)
        self.verticalLayout = QVBoxLayout(SettingsInterface)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cleanDownloadTmpButton = PushButton(SettingsInterface)
        self.cleanDownloadTmpButton.setObjectName(u"cleanDownloadTmpButton")

        self.horizontalLayout.addWidget(self.cleanDownloadTmpButton)

        self.label_2 = QLabel(SettingsInterface)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(SettingsInterface)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 394, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(SettingsInterface)

        QMetaObject.connectSlotsByName(SettingsInterface)
    # setupUi

    def retranslateUi(self, SettingsInterface):
        SettingsInterface.setWindowTitle(QCoreApplication.translate("SettingsInterface", u"Form", None))
        self.cleanDownloadTmpButton.setText(QCoreApplication.translate("SettingsInterface", u"\u6e05\u7406\u4e0b\u8f7d\u6587\u4ef6\u7f13\u5b58", None))
        self.label_2.setText(QCoreApplication.translate("SettingsInterface", u"<html><head/><body><p><span style=\" color:#ff0000;\">\u8b66\u544a\uff1a\u8bf7\u52ff\u5728\u6709\u5b89\u88c5\u4efb\u52a1\u65f6\u6e05\u7406\uff01</span></p></body></html>", None))
        self.label.setText("")
    # retranslateUi

