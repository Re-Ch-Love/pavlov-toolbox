# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'local_mods_manager_interface.ui'
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
    QSpacerItem, QTableWidgetItem, QVBoxLayout, QWidget)

from qfluentwidgets import (PrimaryPushButton, TableWidget)

class Ui_LocalModsManagerInterface(object):
    def setupUi(self, LocalModsManagerInterface):
        if not LocalModsManagerInterface.objectName():
            LocalModsManagerInterface.setObjectName(u"LocalModsManagerInterface")
        LocalModsManagerInterface.resize(865, 456)
        self.verticalLayout = QVBoxLayout(LocalModsManagerInterface)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.updateAllButton = PrimaryPushButton(LocalModsManagerInterface)
        self.updateAllButton.setObjectName(u"updateAllButton")

        self.horizontalLayout.addWidget(self.updateAllButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.modTable = TableWidget(LocalModsManagerInterface)
        if (self.modTable.columnCount() < 3):
            self.modTable.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.modTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.modTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.modTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.modTable.setObjectName(u"modTable")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modTable.sizePolicy().hasHeightForWidth())
        self.modTable.setSizePolicy(sizePolicy)
        self.modTable.horizontalHeader().setStretchLastSection(True)
        self.modTable.verticalHeader().setVisible(False)
        self.modTable.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.modTable)


        self.retranslateUi(LocalModsManagerInterface)

        QMetaObject.connectSlotsByName(LocalModsManagerInterface)
    # setupUi

    def retranslateUi(self, LocalModsManagerInterface):
        LocalModsManagerInterface.setWindowTitle(QCoreApplication.translate("LocalModsManagerInterface", u"Form", None))
        self.updateAllButton.setText(QCoreApplication.translate("LocalModsManagerInterface", u"\u5168\u90e8\u66f4\u65b0", None))
        ___qtablewidgetitem = self.modTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("LocalModsManagerInterface", u"\u64cd\u4f5c", None));
        ___qtablewidgetitem1 = self.modTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("LocalModsManagerInterface", u"\u8d44\u6e90ID", None));
        ___qtablewidgetitem2 = self.modTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("LocalModsManagerInterface", u"\u540d\u79f0", None));
    # retranslateUi

