# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PluginChoucas
                                 A QGIS plugin
 Ce plugin permet :
    - le chargement et 
    - la visualisation 
 de donnees de montagne provenant de differentes API
 
                              -------------------
        begin                : 2017-03-15
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Coline Eva Sylvain
        email                : eva.chenyensu@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtGui import QMessageBox
from qgis.core import QgsVectorLayer
from qgis.core import QgsMapLayerRegistry

# import pour le mode en ligne
import json

# import pour la connection a la bdd
import db_manager.db_plugins.postgis.connector as con
from PyQt4.QtSql import *
#from QtSql import *
#import psycopg2

# Initialize Qt resources from file resources.py
import resources

# Import the code for the dialog
#from plugin_choucas_dialog import PluginChoucasDialog
from gui.plugin_choucas_dialog import PluginChoucasDialog

import os.path
import xml.etree.ElementTree as ET
import os

from data import offline as offline
from data import online as online
from data import util as util

# ------------------------------------------------------------
#
# ------------------------------------------------------------
class PluginChoucas:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PluginChoucas_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = PluginChoucasDialog()
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&CHOUCAS')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PluginChoucas')
        self.toolbar.setObjectName(u'PluginChoucas')

        # On affiche un fond de carte de la France par défaut
        uri = os.path.join(os.path.dirname(__file__) + str('/fond_de_carte/'),'France.shp')
        vlayer = QgsVectorLayer(uri, "France", "ogr")
        # symbol = QgsMarkerSymbolV2.createSimple({'name': '', 'color': 'land' })
        # vlayer.rendererV2().setSymbol(symbol)
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)

        # On connecte les boutons [En ligne] et [Hors ligne] a la fonction permettant de remplir la 1ere comboBox (source)
        self.dlg.radioButton_online.toggled.connect(self.fill_comboBox)
        self.dlg.radioButton_offline.toggled.connect(self.fill_comboBox)

        # On remplit la deuxieme comboBox (entites) a partir de la source selectionee
        self.dlg.comboBox_sources.currentIndexChanged.connect(self.second_list)

        # Des que l utilisateur clique sur Ajouter c est la fonction run_choucas qui est lancee
        self.dlg.pushButton_add.clicked.connect(self.run_choucas)
        # self.dlg.button_box.accepted.connect(self.run)


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PluginChoucas', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.
        """

        # Create the dialog (after translation) and keep reference
        #self.dlg = PluginChoucasDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/PluginChoucas/img/loaddata.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Chargement de données de montagne'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&CHOUCAS'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # On vide les combobox a chaque appel au plugin
        self.dlg.comboBox_sources.clear()
        self.dlg.comboBox_entities.clear()
        # Au moins un des deux boutons devra obligatoirement etre coche au lancement
        self.dlg.radioButton_offline.setChecked(True)
        self.dlg.radioButton_online.setChecked(True)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            pass


    def run_choucas(self):
        """
        Fonction qui permet d afficher les donnees voulues 
        en fonction du mode choisi (en ligne ou hors ligne)
        """
        # On recupere le departement selectione
        selectedDeptIndex = self.dlg.comboBox_dept.currentIndex()
        selectedDept = self.list_dept[selectedDeptIndex]
        self.dept = selectedDept
        # On recupere la source selectionee
        selectedSourceIndex = self.dlg.comboBox_sources.currentIndex()
        selectedSource = self.list_sources[selectedSourceIndex]
        self.source = selectedSource
        # On recupere l entite selectionee
        selectedEntityIndex = self.dlg.comboBox_entities.currentIndex()
        selectedEntity = self.list_entities[selectedEntityIndex]
        self.type_pt = selectedEntity

        # On definit le proxy
        util.chargeProxy(self.dlg.checkBox_proxy)
        
        # On ne peut pas choisir le departement pour les itineraires (avec l api utilisee)
        if self.source == 'vercors rando' and (self.dept != 'Isere' and self.dept != 'Drome'):
            QMessageBox.information(None, "OUPS:", 'Departement non disponible pour cet API')
        # elif self.source == 'vercors rando' and (self.dept == 'Isere' or self.dept == 'Drome'):
        #     if self.dlg.radioButton_online.isChecked():
        #          self.online(self.dept,self.source, self.type_pt)
        else:
            # Si le mode choisi est [En ligne]
            if self.dlg.radioButton_online.isChecked():
                 online.online(self.root, self.list_dept, self.dept, self.source, self.type_pt, self.list_bbox, self.list_admin_area)

        # Si le mode choisi est [Hors ligne]
        if self.dlg.radioButton_offline.isChecked():
             offline.offline(self.root, self.source, self.type_pt)




    def fill_comboBox(self):
        """
        Fonction qui remplit la premiere comboBox (liste des sources disponibles)
        """
        self.dlg.comboBox_sources.clear()
        self.dlg.comboBox_entities.clear()
        self.dlg.comboBox_dept.clear()

        # Liste des departements
        self.list_dept = ['Ain', 'Ardeche', 'Drome', 'Isere', 'Loire', 'Rhone', 'Savoie', 'Haute-savoie']
        # Liste des bounding box
        self.list_bbox = ['4.7279,45.6108,6.1701,46.5199', '3.8611,44.2643,4.8862,45.3662',
'4.6469,44.1152,5.8304,45.344', '4.7416,44.6959,6.3581,45.8836',
'3.6884,45.2311,4.7608,46.2765', '4.5955,43.332,6.0319,46.1932',
'5.6218,45.0516,7.1859,45.9385', '5.8051,45.6817,7.0444,46.4564']
        # Liste des limites administratives
        self.list_admin_area = ['14370', '14359', '14342', '14328', '14325', '14299', '14295', '14366']


        # Si le mode [En ligne] est selectionne
        if self.dlg.radioButton_online.isChecked():
            # On remplit la combobox des departements
            self.dlg.comboBox_dept.addItems(self.list_dept)
            # On va chercher le catalogue associe et on le parse
            f = open(os.path.join(os.path.dirname(__file__), 'catalogue/catalogue.xml'), 'r')
            self.tree = ET.parse(f)
        # Sinon
        else:
            f = open(os.path.join(os.path.dirname(__file__), 'catalogue/catalogue_hl.xml'), 'r')
            self.tree = ET.parse(f)

        self.root = self.tree.getroot()
        l1 = []
        # On recupere toutes les sources disponibles
        for child in self.root:
            name = child.get('name')
            l1.append(name)

        self.list_sources = l1
        # Et on les ajoute a la combobox
        self.dlg.comboBox_sources.addItems(self.list_sources)



    def update_list(self,source) :
        """
        Cette fonction met a jour la liste des donnees disponibles en
        fonction de la source choisie
        source: source selectionnee par l utilisateur
        """
        l2 = []
        # On va recuperer dans le catalogue la source selectionnee
        for child in self.root:
            name = child.get('name')
            # On va chercher le type de donnees disponibles pour la source selectionnee
            if str(name) == str(source):
                for typ in child.iter('type'):
                    typ = typ.get('data-id')
                    l2.append(typ)
        return l2


    def second_list(self):
        """
        Cette fonction remplit la deuxieme comboBox (liste des entites disponibles)
        """
        # On recupere la source selectionnee dans le plugin
        self.source =  self.dlg.comboBox_sources.currentText()
        # On definit la liste des entites en fonction de cette derniere
        self.list_entities =  self.update_list(self.source)
        self.dlg.comboBox_entities.clear()
        # On propose une liste deroulante des types de donnees
        self.dlg.comboBox_entities.addItems(self.list_entities)



    