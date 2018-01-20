# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recherche_motcle_dialog_base.ui'
#
# Created: Sat Jan 20 21:32:41 2018
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
        DockWidget.resize(359, 210)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.boutonCalculer = QtGui.QPushButton(self.dockWidgetContents)
        self.boutonCalculer.setGeometry(QtCore.QRect(240, 140, 101, 23))
        self.boutonCalculer.setObjectName(_fromUtf8("boutonCalculer"))
        self.label_7 = QtGui.QLabel(self.dockWidgetContents)
        self.label_7.setGeometry(QtCore.QRect(20, 60, 101, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.dockWidgetContents)
        self.label_8.setGeometry(QtCore.QRect(20, 20, 91, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.comboAttribut = QtGui.QComboBox(self.dockWidgetContents)
        self.comboAttribut.setGeometry(QtCore.QRect(130, 60, 171, 20))
        self.comboAttribut.setObjectName(_fromUtf8("comboAttribut"))
        self.comboLayer = QtGui.QComboBox(self.dockWidgetContents)
        self.comboLayer.setGeometry(QtCore.QRect(130, 20, 171, 20))
        self.comboLayer.setObjectName(_fromUtf8("comboLayer"))
        self.boutonRAZ = QtGui.QPushButton(self.dockWidgetContents)
        self.boutonRAZ.setGeometry(QtCore.QRect(130, 140, 101, 23))
        self.boutonRAZ.setObjectName(_fromUtf8("boutonRAZ"))
        self.boutonQuitter = QtGui.QPushButton(self.dockWidgetContents)
        self.boutonQuitter.setGeometry(QtCore.QRect(20, 140, 101, 23))
        self.boutonQuitter.setObjectName(_fromUtf8("boutonQuitter"))
        self.label_9 = QtGui.QLabel(self.dockWidgetContents)
        self.label_9.setGeometry(QtCore.QRect(20, 100, 101, 20))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.editMotCle = QtGui.QLineEdit(self.dockWidgetContents)
        self.editMotCle.setGeometry(QtCore.QRect(130, 100, 171, 22))
        self.editMotCle.setObjectName(_fromUtf8("editMotCle"))
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "Recherche par mots clés", None))
        self.boutonCalculer.setText(_translate("DockWidget", "Filtrer", None))
        self.label_7.setText(_translate("DockWidget", "Attribut :", None))
        self.label_8.setText(_translate("DockWidget", "Layer :", None))
        self.boutonRAZ.setText(_translate("DockWidget", "RAZ", None))
        self.boutonQuitter.setText(_translate("DockWidget", "Quitter", None))
        self.label_9.setText(_translate("DockWidget", "Mot clé :", None))

