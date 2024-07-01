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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QVBoxLayout,
    QWidget)

from qfluentwidgets import (CaptionLabel, CardWidget, ProgressBar, StrongBodyLabel,
    TransparentToolButton)

class Ui_DownloadCard(object):
    def setupUi(self, DownloadCard):
        if not DownloadCard.objectName():
            DownloadCard.setObjectName(u"DownloadCard")
        DownloadCard.resize(416, 131)
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
        self.nameLabel = StrongBodyLabel(self.frame)
        self.nameLabel.setObjectName(u"nameLabel")

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
        self.progressBar.setValue(88)

        self.horizontalLayout_2.addWidget(self.progressBar)

        self.percentageLabel = CaptionLabel(self.frame)
        self.percentageLabel.setObjectName(u"percentageLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.percentageLabel.sizePolicy().hasHeightForWidth())
        self.percentageLabel.setSizePolicy(sizePolicy1)
        self.percentageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.percentageLabel)

        self.rateLabel = CaptionLabel(self.frame)
        self.rateLabel.setObjectName(u"rateLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.rateLabel.sizePolicy().hasHeightForWidth())
        self.rateLabel.setSizePolicy(sizePolicy2)
        self.rateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.rateLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addWidget(self.frame)


        self.retranslateUi(DownloadCard)

        QMetaObject.connectSlotsByName(DownloadCard)
    # setupUi

    def retranslateUi(self, DownloadCard):
        DownloadCard.setWindowTitle(QCoreApplication.translate("DownloadCard", u"Form", None))
        self.nameLabel.setText(QCoreApplication.translate("DownloadCard", u"TextLabel", None))
        self.toggleButton.setText("")
        self.closeButton.setText("")
        self.progressBar.setFormat("")
        self.percentageLabel.setText(QCoreApplication.translate("DownloadCard", u"88%", None))
        self.rateLabel.setText(QCoreApplication.translate("DownloadCard", u"10.0MB/s", None))
    # retranslateUi

