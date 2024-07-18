# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_webview_toolbox.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QWidget)

from qfluentwidgets import (CaptionLabel, ToolButton)

class Ui_AppWebviewToolbox(object):
    def setupUi(self, AppWebviewToolbox):
        if not AppWebviewToolbox.objectName():
            AppWebviewToolbox.setObjectName(u"AppWebviewToolbox")
        AppWebviewToolbox.resize(542, 22)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AppWebviewToolbox.sizePolicy().hasHeightForWidth())
        AppWebviewToolbox.setSizePolicy(sizePolicy)
        AppWebviewToolbox.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(AppWebviewToolbox)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, 1, 6, 1)
        self.label = CaptionLabel(AppWebviewToolbox)
        self.label.setObjectName(u"label")
        self.label.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.label)

        self.homeButton = ToolButton(AppWebviewToolbox)
        self.homeButton.setObjectName(u"homeButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.homeButton.sizePolicy().hasHeightForWidth())
        self.homeButton.setSizePolicy(sizePolicy2)
        self.homeButton.setStyleSheet(u"border: none;")

        self.horizontalLayout.addWidget(self.homeButton)

        self.backButton = ToolButton(AppWebviewToolbox)
        self.backButton.setObjectName(u"backButton")
        sizePolicy2.setHeightForWidth(self.backButton.sizePolicy().hasHeightForWidth())
        self.backButton.setSizePolicy(sizePolicy2)
        self.backButton.setStyleSheet(u"border: none;")

        self.horizontalLayout.addWidget(self.backButton, 0, Qt.AlignmentFlag.AlignVCenter)

        self.forwardButton = ToolButton(AppWebviewToolbox)
        self.forwardButton.setObjectName(u"forwardButton")
        sizePolicy2.setHeightForWidth(self.forwardButton.sizePolicy().hasHeightForWidth())
        self.forwardButton.setSizePolicy(sizePolicy2)
        self.forwardButton.setStyleSheet(u"border: none;")

        self.horizontalLayout.addWidget(self.forwardButton)


        self.retranslateUi(AppWebviewToolbox)

        QMetaObject.connectSlotsByName(AppWebviewToolbox)
    # setupUi

    def retranslateUi(self, AppWebviewToolbox):
        AppWebviewToolbox.setWindowTitle(QCoreApplication.translate("AppWebviewToolbox", u"Form", None))
        self.label.setText(QCoreApplication.translate("AppWebviewToolbox", u"TextLabel", None))
        self.homeButton.setText("")
        self.backButton.setText("")
        self.forwardButton.setText("")
    # retranslateUi

