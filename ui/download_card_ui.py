# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'download_card.ui'
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
    QVBoxLayout, QWidget)

from qfluentwidgets import (CaptionLabel, CardWidget, ProgressBar, TransparentToolButton)

class Ui_DownloadCard(object):
    def setupUi(self, DownloadCard):
        if not DownloadCard.objectName():
            DownloadCard.setObjectName(u"DownloadCard")
        DownloadCard.resize(526, 118)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DownloadCard.sizePolicy().hasHeightForWidth())
        DownloadCard.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(DownloadCard)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = CardWidget(DownloadCard)
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

        self.toggleButton = TransparentToolButton(self.frame)
        self.toggleButton.setObjectName(u"toggleButton")

        self.horizontalLayout.addWidget(self.toggleButton)

        self.closeButton = TransparentToolButton(self.frame)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.progressBar = ProgressBar(self.frame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximum(1000)
        self.progressBar.setValue(88)

        self.horizontalLayout_2.addWidget(self.progressBar)

        self.progressLabel = CaptionLabel(self.frame)
        self.progressLabel.setObjectName(u"progressLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.progressLabel.sizePolicy().hasHeightForWidth())
        self.progressLabel.setSizePolicy(sizePolicy2)
        self.progressLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.progressLabel)

        self.speedLabel = CaptionLabel(self.frame)
        self.speedLabel.setObjectName(u"speedLabel")
        sizePolicy2.setHeightForWidth(self.speedLabel.sizePolicy().hasHeightForWidth())
        self.speedLabel.setSizePolicy(sizePolicy2)
        self.speedLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.speedLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addWidget(self.frame)


        self.retranslateUi(DownloadCard)

        QMetaObject.connectSlotsByName(DownloadCard)
    # setupUi

    def retranslateUi(self, DownloadCard):
        DownloadCard.setWindowTitle(QCoreApplication.translate("DownloadCard", u"Form", None))
        self.nameLabel.setText(QCoreApplication.translate("DownloadCard", u"<html><head/><body><p><span style=\" font-size:16pt;\">\u6587\u4ef6\u540d</span><span style=\" font-size:10pt; color:#737373;\">\uff08\u63d0\u793a\u6587\u4ef6\u540d\uff09</span></p></body></html>", None))
        self.toggleButton.setText("")
        self.closeButton.setText("")
        self.progressBar.setFormat("")
        self.progressLabel.setText(QCoreApplication.translate("DownloadCard", u"- B / - B", None))
        self.speedLabel.setText(QCoreApplication.translate("DownloadCard", u"- B/s", None))
    # retranslateUi

