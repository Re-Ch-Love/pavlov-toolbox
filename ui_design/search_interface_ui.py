# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search_interface.ui'
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

from qfluentwidgets import (CaptionLabel, RadioButton, SearchLineEdit, TableWidget)

class Ui_SearchInterface(object):
    def setupUi(self, SearchInterface):
        if not SearchInterface.objectName():
            SearchInterface.setObjectName(u"SearchInterface")
        SearchInterface.resize(776, 474)
        self.verticalLayout = QVBoxLayout(SearchInterface)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.searchLineEdit = SearchLineEdit(SearchInterface)
        self.searchLineEdit.setObjectName(u"searchLineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchLineEdit.sizePolicy().hasHeightForWidth())
        self.searchLineEdit.setSizePolicy(sizePolicy)
        self.searchLineEdit.setMinimumSize(QSize(400, 30))

        self.verticalLayout.addWidget(self.searchLineEdit, 0, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 8, -1, 8)
        self.modNameButton = RadioButton(SearchInterface)
        self.modNameButton.setObjectName(u"modNameButton")
        sizePolicy.setHeightForWidth(self.modNameButton.sizePolicy().hasHeightForWidth())
        self.modNameButton.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.modNameButton)

        self.ridButton = RadioButton(SearchInterface)
        self.ridButton.setObjectName(u"ridButton")
        sizePolicy.setHeightForWidth(self.ridButton.sizePolicy().hasHeightForWidth())
        self.ridButton.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.ridButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.resultTableWidget = TableWidget(SearchInterface)
        if (self.resultTableWidget.columnCount() < 3):
            self.resultTableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.resultTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.resultTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.resultTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.resultTableWidget.setObjectName(u"resultTableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.resultTableWidget.sizePolicy().hasHeightForWidth())
        self.resultTableWidget.setSizePolicy(sizePolicy1)
        self.resultTableWidget.horizontalHeader().setStretchLastSection(False)
        self.resultTableWidget.verticalHeader().setVisible(False)
        self.resultTableWidget.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.resultTableWidget)

        self.label = CaptionLabel(SearchInterface)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)


        self.retranslateUi(SearchInterface)

        QMetaObject.connectSlotsByName(SearchInterface)
    # setupUi

    def retranslateUi(self, SearchInterface):
        SearchInterface.setWindowTitle(QCoreApplication.translate("SearchInterface", u"Form", None))
        self.searchLineEdit.setPlaceholderText("")
        self.modNameButton.setText(QCoreApplication.translate("SearchInterface", u"\u6839\u636eMod\u540d\u79f0\u641c\u7d22", None))
        self.ridButton.setText(QCoreApplication.translate("SearchInterface", u"\u6839\u636eMod\u8d44\u6e90ID\u641c\u7d22", None))
        ___qtablewidgetitem = self.resultTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("SearchInterface", u"\u64cd\u4f5c", None));
        ___qtablewidgetitem1 = self.resultTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("SearchInterface", u"\u8d44\u6e90ID", None));
        ___qtablewidgetitem2 = self.resultTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("SearchInterface", u"\u540d\u79f0", None));
        self.label.setText(QCoreApplication.translate("SearchInterface", u"\u63d0\u793a\uff1a\u5de6\u952e\u5355\u51fb\u5355\u5143\u683c\u540e\uff0c\u53ef\u4ee5\u4f7f\u7528 Ctrl+C \u590d\u5236\u5185\u5bb9", None))
    # retranslateUi

