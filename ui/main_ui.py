# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 494)
        self.act_getModDlUrl = QAction(MainWindow)
        self.act_getModDlUrl.setObjectName(u"act_getModDlUrl")
        self.act_unzipAndCompletion = QAction(MainWindow)
        self.act_unzipAndCompletion.setObjectName(u"act_unzipAndCompletion")
        self.act_search = QAction(MainWindow)
        self.act_search.setObjectName(u"act_search")
        self.action_4 = QAction(MainWindow)
        self.action_4.setObjectName(u"action_4")
        self.act_notice = QAction(MainWindow)
        self.act_notice.setObjectName(u"act_notice")
        self.act_checkUpdates = QAction(MainWindow)
        self.act_checkUpdates.setObjectName(u"act_checkUpdates")
        self.act_usage = QAction(MainWindow)
        self.act_usage.setObjectName(u"act_usage")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menu_functions = QMenu(self.menubar)
        self.menu_functions.setObjectName(u"menu_functions")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_functions.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_functions.addAction(self.act_getModDlUrl)
        self.menu_functions.addAction(self.act_unzipAndCompletion)
        self.menu_functions.addAction(self.act_search)
        self.menu_help.addAction(self.act_notice)
        self.menu_help.addAction(self.act_checkUpdates)
        self.menu_help.addSeparator()
        self.menu_help.addAction(self.act_usage)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Pavlov \u5de5\u5177\u7bb1 by Re-Ch", None))
        self.act_getModDlUrl.setText(QCoreApplication.translate("MainWindow", u"\u83b7\u53d6Mod\u4e0b\u8f7d\u94fe\u63a5", None))
        self.act_unzipAndCompletion.setText(QCoreApplication.translate("MainWindow", u"\u89e3\u538b\u5e76\u8865\u5168Mod\u538b\u7f29\u5305", None))
#if QT_CONFIG(tooltip)
        self.act_unzipAndCompletion.setToolTip(QCoreApplication.translate("MainWindow", u"\u89e3\u538b\u5e76\u8865\u5168Mod\u7684Zip\u6587\u4ef6", None))
#endif // QT_CONFIG(tooltip)
        self.act_search.setText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22Mod\u76f8\u5173\u4fe1\u606f", None))
        self.action_4.setText("")
        self.act_notice.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u770b\u516c\u544a", None))
        self.act_checkUpdates.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u67e5\u66f4\u65b0", None))
        self.act_usage.setText(QCoreApplication.translate("MainWindow", u"\u524d\u5f80\u4f7f\u7528\u6307\u5357\u7f51\u7ad9", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">\u6b22\u8fce\u4f7f\u7528 Pavlov \u5de5\u5177\u7bb1</span></p><p align=\"center\"><span style=\" font-size:14pt;\">\u60a8\u53ef\u4ee5\u70b9\u51fb\u5de6\u4e0a\u89d2\u7684 </span><span style=\" font-size:14pt; font-weight:700;\">\u529f\u80fd</span><span style=\" font-size:14pt;\"> \u83dc\u5355\u6765\u9009\u62e9\u9700\u8981\u7684\u529f\u80fd</span></p><p align=\"center\"><span style=\" font-size:14pt;\">\u6216\u662f\u70b9\u51fb </span><span style=\" font-size:14pt; font-weight:700;\">\u5e2e\u52a9 - \u524d\u5f80\u4f7f\u7528\u6307\u5357\u7f51\u7ad9</span><span style=\" font-size:14pt;\"> \u67e5\u770b\u8bf4\u660e</span></p></body></html>", None))
        self.menu_functions.setTitle(QCoreApplication.translate("MainWindow", u"\u529f\u80fd", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

