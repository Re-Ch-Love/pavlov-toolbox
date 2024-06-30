# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home_interface.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QTextBrowser,
    QWidget)

class Ui_HomeInterface(object):
    def setupUi(self, HomeInterface):
        if not HomeInterface.objectName():
            HomeInterface.setObjectName(u"HomeInterface")
        HomeInterface.resize(799, 487)
        self.horizontalLayout = QHBoxLayout(HomeInterface)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.textBrowser = QTextBrowser(HomeInterface)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")

        self.horizontalLayout.addWidget(self.textBrowser)


        self.retranslateUi(HomeInterface)

        QMetaObject.connectSlotsByName(HomeInterface)
    # setupUi

    def retranslateUi(self, HomeInterface):
        HomeInterface.setWindowTitle(QCoreApplication.translate("HomeInterface", u"Form", None))
        self.textBrowser.setHtml(QCoreApplication.translate("HomeInterface", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">\u6b22\u8fce\u4f7f\u7528 Pavlov \u5de5\u5177\u7bb1</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">\u4f5c\u8005\uff1aRe-Ch</span></p></body></html>", None))
    # retranslateUi

