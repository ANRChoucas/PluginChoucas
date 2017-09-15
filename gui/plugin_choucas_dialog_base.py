# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plugin_choucas_dialog_base.ui'
#
# Created: Fri Sep 15 10:36:25 2017
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

class Ui_PluginChoucasDialogBase(object):
    def setupUi(self, PluginChoucasDialogBase):
        PluginChoucasDialogBase.setObjectName(_fromUtf8("PluginChoucasDialogBase"))
        PluginChoucasDialogBase.resize(446, 372)
        self.groupBox = QtGui.QGroupBox(PluginChoucasDialogBase)
        self.groupBox.setEnabled(True)
        self.groupBox.setGeometry(QtCore.QRect(10, 38, 421, 91))
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.rb_online = QtGui.QRadioButton(self.groupBox)
        self.rb_online.setGeometry(QtCore.QRect(20, 60, 117, 22))
        self.rb_online.setChecked(True)
        self.rb_online.setObjectName(_fromUtf8("rb_online"))
        self.rb_offline = QtGui.QRadioButton(self.groupBox)
        self.rb_offline.setGeometry(QtCore.QRect(20, 20, 117, 22))
        self.rb_offline.setObjectName(_fromUtf8("rb_offline"))
        self.cb_proxy = QtGui.QCheckBox(self.groupBox)
        self.cb_proxy.setGeometry(QtCore.QRect(100, 60, 99, 22))
        self.cb_proxy.setChecked(True)
        self.cb_proxy.setObjectName(_fromUtf8("cb_proxy"))
        self.rb_local = QtGui.QRadioButton(self.groupBox)
        self.rb_local.setGeometry(QtCore.QRect(20, 40, 117, 22))
        self.rb_local.setObjectName(_fromUtf8("rb_local"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(100, 22, 101, 16))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(100, 40, 101, 16))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.boutonAdd = QtGui.QPushButton(PluginChoucasDialogBase)
        self.boutonAdd.setGeometry(QtCore.QRect(210, 330, 99, 27))
        self.boutonAdd.setObjectName(_fromUtf8("boutonAdd"))
        self.label_5 = QtGui.QLabel(PluginChoucasDialogBase)
        self.label_5.setGeometry(QtCore.QRect(20, 10, 81, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.cb_fondcarte = QtGui.QCheckBox(PluginChoucasDialogBase)
        self.cb_fondcarte.setGeometry(QtCore.QRect(120, 10, 171, 17))
        self.cb_fondcarte.setChecked(False)
        self.cb_fondcarte.setObjectName(_fromUtf8("cb_fondcarte"))
        self.boutonClose = QtGui.QPushButton(PluginChoucasDialogBase)
        self.boutonClose.setGeometry(QtCore.QRect(320, 330, 93, 28))
        self.boutonClose.setObjectName(_fromUtf8("boutonClose"))
        self.groupBox_2 = QtGui.QGroupBox(PluginChoucasDialogBase)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 140, 421, 171))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 101, 41))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.comboEntities = QtGui.QComboBox(self.groupBox_2)
        self.comboEntities.setGeometry(QtCore.QRect(130, 70, 181, 31))
        self.comboEntities.setObjectName(_fromUtf8("comboEntities"))
        self.comboSources = QtGui.QComboBox(self.groupBox_2)
        self.comboSources.setGeometry(QtCore.QRect(130, 30, 181, 31))
        self.comboSources.setObjectName(_fromUtf8("comboSources"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(30, 60, 101, 41))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 111, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.comboEmprise = QtGui.QComboBox(self.groupBox_2)
        self.comboEmprise.setGeometry(QtCore.QRect(130, 120, 181, 31))
        self.comboEmprise.setEditable(False)
        self.comboEmprise.setObjectName(_fromUtf8("comboEmprise"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(30, 140, 81, 16))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.cb_emprise_affiche = QtGui.QCheckBox(self.groupBox_2)
        self.cb_emprise_affiche.setGeometry(QtCore.QRect(320, 128, 70, 17))
        font = QtGui.QFont()
        font.setItalic(True)
        self.cb_emprise_affiche.setFont(font)
        self.cb_emprise_affiche.setObjectName(_fromUtf8("cb_emprise_affiche"))

        self.retranslateUi(PluginChoucasDialogBase)
        QtCore.QMetaObject.connectSlotsByName(PluginChoucasDialogBase)

    def retranslateUi(self, PluginChoucasDialogBase):
        PluginChoucasDialogBase.setWindowTitle(_translate("PluginChoucasDialogBase", "CHOUCAS", None))
        self.groupBox.setTitle(_translate("PluginChoucasDialogBase", "Mode de connexion", None))
        self.rb_online.setText(_translate("PluginChoucasDialogBase", "En ligne", None))
        self.rb_offline.setText(_translate("PluginChoucasDialogBase", "Hors ligne", None))
        self.cb_proxy.setText(_translate("PluginChoucasDialogBase", "Proxy IGN", None))
        self.rb_local.setText(_translate("PluginChoucasDialogBase", "Local", None))
        self.label_6.setText(_translate("PluginChoucasDialogBase", "(base de données)", None))
        self.label_7.setText(_translate("PluginChoucasDialogBase", "(shapefile)", None))
        self.boutonAdd.setText(_translate("PluginChoucasDialogBase", "Ajouter", None))
        self.label_5.setText(_translate("PluginChoucasDialogBase", "Fond carto :", None))
        self.cb_fondcarte.setText(_translate("PluginChoucasDialogBase", "France métropolitaine", None))
        self.boutonClose.setText(_translate("PluginChoucasDialogBase", "Fermer", None))
        self.groupBox_2.setTitle(_translate("PluginChoucasDialogBase", "Données à charger", None))
        self.label_3.setText(_translate("PluginChoucasDialogBase", "Emprise à prendre :", None))
        self.label.setText(_translate("PluginChoucasDialogBase", "Entités à afficher :", None))
        self.label_2.setText(_translate("PluginChoucasDialogBase", "Origine des entités :", None))
        self.label_4.setText(_translate("PluginChoucasDialogBase", "(suivant la bbox)", None))
        self.cb_emprise_affiche.setText(_translate("PluginChoucasDialogBase", "à afficher", None))

