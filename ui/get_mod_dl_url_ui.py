# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_mod_dl_url.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QPlainTextEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_getModDlUrl(object):
    def setupUi(self, getModDlUrl):
        if not getModDlUrl.objectName():
            getModDlUrl.setObjectName(u"getModDlUrl")
        getModDlUrl.resize(800, 547)
        self.verticalLayout = QVBoxLayout(getModDlUrl)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.ptedit_resourceId = QPlainTextEdit(getModDlUrl)
        self.ptedit_resourceId.setObjectName(u"ptedit_resourceId")

        self.gridLayout.addWidget(self.ptedit_resourceId, 2, 0, 2, 1)

        self.ptedit_dlUrl = QPlainTextEdit(getModDlUrl)
        self.ptedit_dlUrl.setObjectName(u"ptedit_dlUrl")
        self.ptedit_dlUrl.setReadOnly(True)

        self.gridLayout.addWidget(self.ptedit_dlUrl, 3, 2, 1, 1)

        self.lb_dlUrl = QLabel(getModDlUrl)
        self.lb_dlUrl.setObjectName(u"lb_dlUrl")
        font = QFont()
        font.setPointSize(14)
        self.lb_dlUrl.setFont(font)
        self.lb_dlUrl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lb_dlUrl, 0, 2, 1, 1)

        self.pbtn_convert = QPushButton(getModDlUrl)
        self.pbtn_convert.setObjectName(u"pbtn_convert")
        self.pbtn_convert.setFont(font)

        self.gridLayout.addWidget(self.pbtn_convert, 0, 1, 1, 1)

        self.lb_resourceId = QLabel(getModDlUrl)
        self.lb_resourceId.setObjectName(u"lb_resourceId")
        self.lb_resourceId.setFont(font)
        self.lb_resourceId.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lb_resourceId, 0, 0, 1, 1)

        self.pbtn_copy = QPushButton(getModDlUrl)
        self.pbtn_copy.setObjectName(u"pbtn_copy")
        font1 = QFont()
        font1.setPointSize(10)
        self.pbtn_copy.setFont(font1)

        self.gridLayout.addWidget(self.pbtn_copy, 1, 2, 2, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cbbox_modListName = QComboBox(getModDlUrl)
        self.cbbox_modListName.setObjectName(u"cbbox_modListName")

        self.horizontalLayout_3.addWidget(self.cbbox_modListName)

        self.pbtn_replace = QPushButton(getModDlUrl)
        self.pbtn_replace.setObjectName(u"pbtn_replace")
        self.pbtn_replace.setFont(font1)

        self.horizontalLayout_3.addWidget(self.pbtn_replace)


        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(getModDlUrl)

        QMetaObject.connectSlotsByName(getModDlUrl)
    # setupUi

    def retranslateUi(self, getModDlUrl):
        getModDlUrl.setWindowTitle(QCoreApplication.translate("getModDlUrl", u"Form", None))
        self.ptedit_resourceId.setPlaceholderText("")
        self.lb_dlUrl.setText(QCoreApplication.translate("getModDlUrl", u"Mod\u4e0b\u8f7d\u94fe\u63a5", None))
        self.pbtn_convert.setText(QCoreApplication.translate("getModDlUrl", u"\u8f6c\u6362\u5230", None))
        self.lb_resourceId.setText(QCoreApplication.translate("getModDlUrl", u"\u8d44\u6e90ID", None))
        self.pbtn_copy.setText(QCoreApplication.translate("getModDlUrl", u"\u590d\u5236\u5230\u526a\u8d34\u677f", None))
        self.pbtn_replace.setText(QCoreApplication.translate("getModDlUrl", u"\u4e00\u952e\u586b\u5145", None))
    # retranslateUi

