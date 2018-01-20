# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'afficher_description_dialog_base.ui'
#
# Created: Sat Jan 20 21:32:45 2018
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(368, 390)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.label_8 = QtGui.QLabel(self.dockWidgetContents)
        self.label_8.setGeometry(QtCore.QRect(20, 10, 91, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.boutonQuitter = QtGui.QPushButton(self.dockWidgetContents)
        self.boutonQuitter.setGeometry(QtCore.QRect(240, 320, 101, 23))
        self.boutonQuitter.setObjectName(_fromUtf8("boutonQuitter"))
        self.plainTextEdit = QtGui.QPlainTextEdit(self.dockWidgetContents)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 40, 321, 271))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "Description de l\'itinéraire", None))
        self.label_8.setText(_translate("DockWidget", "Description :", None))
        self.boutonQuitter.setText(_translate("DockWidget", "Quitter", None))

