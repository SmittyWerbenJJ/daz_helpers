# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(466, 396)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listbox = QListWidget(Dialog)
        self.listbox.setObjectName(u"listbox")
        self.listbox.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout.addWidget(self.listbox)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_select_all = QPushButton(self.groupBox)
        self.btn_select_all.setObjectName(u"btn_select_all")

        self.horizontalLayout_3.addWidget(self.btn_select_all)

        self.btn_select_none = QPushButton(self.groupBox)
        self.btn_select_none.setObjectName(u"btn_select_none")

        self.horizontalLayout_3.addWidget(self.btn_select_none)

        self.btn_select_invert = QPushButton(self.groupBox)
        self.btn_select_invert.setObjectName(u"btn_select_invert")

        self.horizontalLayout_3.addWidget(self.btn_select_invert)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btn_open_selected_in_everything = QPushButton(self.groupBox)
        self.btn_open_selected_in_everything.setObjectName(u"btn_open_selected_in_everything")

        self.gridLayout.addWidget(self.btn_open_selected_in_everything, 0, 1, 1, 1)

        self.btn_open_all_in_everything = QPushButton(self.groupBox)
        self.btn_open_all_in_everything.setObjectName(u"btn_open_all_in_everything")

        self.gridLayout.addWidget(self.btn_open_all_in_everything, 0, 0, 1, 1)

        self.btn_copy_to_clipboard = QPushButton(self.groupBox)
        self.btn_copy_to_clipboard.setObjectName(u"btn_copy_to_clipboard")

        self.gridLayout.addWidget(self.btn_copy_to_clipboard, 0, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout.addWidget(self.groupBox)


        self.retranslateUi(Dialog)
        self.btn_open_selected_in_everything.clicked.connect(Dialog.open_selected_in_everything)
        self.btn_open_all_in_everything.clicked.connect(Dialog.open_all_in_everything)
        self.btn_copy_to_clipboard.clicked.connect(Dialog.copy_To_Clipboard)
        self.btn_select_all.clicked.connect(Dialog.select_all)
        self.btn_select_invert.clicked.connect(Dialog.select_invert)
        self.btn_select_none.clicked.connect(Dialog.select_none)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Tools", None))
        self.btn_select_all.setText(QCoreApplication.translate("Dialog", u"Select: All", None))
        self.btn_select_none.setText(QCoreApplication.translate("Dialog", u"Select: None", None))
        self.btn_select_invert.setText(QCoreApplication.translate("Dialog", u"Select: Invert", None))
        self.btn_open_selected_in_everything.setText(QCoreApplication.translate("Dialog", u"Open selected in Everything", None))
        self.btn_open_all_in_everything.setText(QCoreApplication.translate("Dialog", u"Open all in Everything", None))
        self.btn_copy_to_clipboard.setText(QCoreApplication.translate("Dialog", u"Copy All to Clipboard", None))
    # retranslateUi

