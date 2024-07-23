# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'installation_card.ui'
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

from qfluentwidgets import (CaptionLabel, CardWidget, TransparentToolButton)

class Ui_InstallationCard(object):
    def setupUi(self, InstallationCard):
        if not InstallationCard.objectName():
            InstallationCard.setObjectName(u"InstallationCard")
        InstallationCard.resize(526, 126)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InstallationCard.sizePolicy().hasHeightForWidth())
        InstallationCard.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(InstallationCard)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = CardWidget(InstallationCard)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(0, 100))
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(15, 15, 15, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.nameLabel = QLabel(self.frame)
        self.nameLabel.setObjectName(u"nameLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.nameLabel.sizePolicy().hasHeightForWidth())
        self.nameLabel.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(9)
        self.nameLabel.setFont(font)
        self.nameLabel.setStyleSheet(u"")
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.nameLabel)

        self.closeButton = TransparentToolButton(self.frame)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.progressBarHLayout = QHBoxLayout()
        self.progressBarHLayout.setObjectName(u"progressBarHLayout")

        self.verticalLayout.addLayout(self.progressBarHLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.promptLabel = CaptionLabel(self.frame)
        self.promptLabel.setObjectName(u"promptLabel")

        self.horizontalLayout_3.addWidget(self.promptLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.progressInfoLabel = CaptionLabel(self.frame)
        self.progressInfoLabel.setObjectName(u"progressInfoLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.progressInfoLabel.sizePolicy().hasHeightForWidth())
        self.progressInfoLabel.setSizePolicy(sizePolicy2)
        self.progressInfoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.progressInfoLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addWidget(self.frame)


        self.retranslateUi(InstallationCard)

        QMetaObject.connectSlotsByName(InstallationCard)
    # setupUi

    def retranslateUi(self, InstallationCard):
        InstallationCard.setWindowTitle(QCoreApplication.translate("InstallationCard", u"Form", None))
        self.nameLabel.setText(QCoreApplication.translate("InstallationCard", u"<html><head/><body><p><span style=\" font-size:16pt;\">\u6587\u4ef6\u540d</span><span style=\" font-size:10pt; color:#737373;\">\uff08\u63d0\u793a\u6587\u4ef6\u540d\uff09</span></p></body></html>", None))
        self.closeButton.setText("")
        self.promptLabel.setText(QCoreApplication.translate("InstallationCard", u"\u901a\u8fc7xxxxx\u52a0\u901f\u4e2d", None))
        self.progressInfoLabel.setText(QCoreApplication.translate("InstallationCard", u"- B / - B  - B /s", None))
    # retranslateUi

