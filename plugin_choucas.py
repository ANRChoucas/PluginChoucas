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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt 
# from PyQt4.QtCore import QFile, QFileInfo
from PyQt4.QtGui import QAction, QIcon
# from PyQt4.QtGui import QMessageBox
from qgis.core import QgsVectorLayer, QgsMapLayer
from qgis.core import QgsMapLayerRegistry

# Initialize Qt resources from file resources.py
from resources import resources

# Import the code for the dialog
from gui.plugin_choucas_dialog import PluginChoucasDialog
from gui.recherche_motcle_dialog import RechercheMotcleDialog
from gui.afficher_description_dialog import AfficherDescriptionDialog

import os.path
import xml.etree.ElementTree as ET
import os

from api import offline as offline
from api import online as online
from api import osm as osm
from api import local as local
from api import util
from api import bbox

# ------------------------------------------------------------
#
# ------------------------------------------------------------
class PluginChoucas:
    """QGIS Plugin Implementation."""

    # Constructor.
    def __init__(self, iface):
        
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

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&CHOUCAS')

        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PluginChoucas')
        self.toolbar.setObjectName(u'PluginChoucas')

        self.pluginIsActive = False
        self.dlg = None
        
        #self.plugin2IsActive = False
        #self.dockwidget = None
        
        self.pluginMotCleIsActive = False
        self.dlgMotCle = None
        
        self.pluginDescriptionIsActive = False
        self.dlgDesc = None
        
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
        # self.dlg = PluginChoucasDialog()

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
        
        icon_path = ':/plugins/PluginChoucas/img/loupe.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Recherche par mots sur clé'),
            callback=self.search,
            parent=self.iface.mainWindow())
        
        #icon_path = ':/plugins/PluginChoucas/img/landmark.png'
        #self.add_action(
        #    icon_path,
        #    text=self.tr(u'Afficher la description de l itinéraire'),
        #    callback=self.displayDescription,
        #    parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&CHOUCAS'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def onClosePlugin(self):
        
        # disconnects
        #self.dlg.boutonClose.disconnect(self.onClosePlugin)

        self.pluginIsActive = False
        self.dlg.close()
        
        self.plugin2IsActive = False
        
        # disconnects
        #self.dlg.closingPlugin.disconnect(self.onClosePlugin)


    # Quand on appuie sur le bouton "Chargement" de la barre de menu
    def run(self):
        
        if not self.pluginIsActive:
            self.pluginIsActive = True       
       
            if self.dlg == None:
                self.dlg = PluginChoucasDialog()
                
                # On vide les combobox a chaque appel au plugin
                self.dlg.comboSources.clear()
                self.dlg.comboEntities.clear()
                self.dlg.comboEmprise.clear()
                
                # On initialise les listes
                self.fillSource()
                self.fillEntities()
        
                # On connecte les boutons [En ligne] et [Hors ligne] 
                #    a la fonction permettant de remplir la 1ere comboBox (source)
                self.dlg.rb_online.clicked.connect(self.fillSource)
                self.dlg.rb_offline.clicked.connect(self.fillSource)
                self.dlg.rb_local.clicked.connect(self.fillSource)
                
                # On remplit la deuxieme comboBox (entites) a partir de la source selectionee
                self.dlg.comboSources.currentIndexChanged.connect(self.fillEntities)
                #self.dlg.comboSources.currentIndexChanged.connect(self.fillEmprise)
                
                # Au moins un des deux boutons devra obligatoirement etre coche au lancement
                self.dlg.rb_offline.setChecked(False)
                self.dlg.rb_local.setChecked(False)
                self.dlg.rb_online.setChecked(True)
                
                # Des que l utilisateur clique sur Ajouter c est la fonction run_choucas qui est lancee
                self.dlg.boutonAdd.clicked.connect(self.run_choucas)
        
                self.dlg.boutonClose.clicked.connect(self.onClosePlugin)
                
        # show the dialog
        self.dlg.show()
        
        
    def fillSource(self):
        """
        Fonction qui remplit la premiere comboBox (liste des sources disponibles)
        """
        self.dlg.comboSources.clear()
        self.dlg.comboEntities.clear()
        self.dlg.comboEmprise.clear()
        
        # On va chercher le catalogue associe et on le parse
        if self.dlg.rb_online.isChecked():
            # Si le mode [En ligne] est selectionne
            catalogueFilename = 'resources/catalogue/catalogue_online.xml'
        elif self.dlg.rb_local.isChecked():
            # Sinon [Local]
            catalogueFilename = 'resources/catalogue/catalogue_local.xml'
        else:
            # Sinon [Hors ligne]
            catalogueFilename = 'resources/catalogue/catalogue_offline.xml'
            
            # On grise la liste des emprises non necessaire
            self.dlg.comboEmprise.setEnabled(False)
            self.dlg.comboEmprise.addItem('---')
        
        
        f = open(os.path.join(os.path.dirname(__file__), catalogueFilename), 'r')
        self.tree = ET.parse(f)
        self.root = self.tree.getroot()
        self.list_sources = []
        
        # On recupere toutes les sources disponibles
        for child in self.root:
            name = child.get('name')
            self.list_sources.append(name)
        self.list_sources.sort()
        # Et on les ajoute a la combobox
        self.dlg.comboSources.addItems(self.list_sources)
        
        
        self.fillEntities()
        
        
    def fillEntities(self):
        """
        Cette fonction remplit la deuxieme comboBox (liste des entites disponibles)
        """
        # On recupere la source selectionnee dans le plugin
        source =  self.dlg.comboSources.currentText()
        
        # On definit la liste des entites en fonction de cette derniere
        l2 = []
        # On va recuperer dans le catalogue la source selectionnee
        for child in self.root:
            name = child.get('name')
            # On va chercher le type de donnees disponibles pour la source selectionnee
            if str(name) == str(source):
                for typ in child.iter('type'):
                    typ = typ.get('data-id')
                    l2.append(typ)
        
        self.list_entities =  l2
        
        self.dlg.comboEntities.clear()
        
        # On propose une liste deroulante des types de donnees
        self.dlg.comboEntities.addItems(self.list_entities)
        
        self.fillEmprise()
    
    def fillEmprise(self):
        
        self.dlg.comboEmprise.clear()
        
        if self.dlg.rb_online.isChecked() or self.dlg.rb_local.isChecked():
            # On regarde quel type d'emprise a été choisi
            sourceSelect =  self.dlg.comboSources.currentText()
            # print (sourceSelect)
            if sourceSelect != None and sourceSelect != '':
                empriseSelect = util.get_first_object(self.root, sourceSelect, 'emprise')
            else:
                empriseSelect = 'none' 
        
            # Si EMPRISE == BBox
            if empriseSelect == 'none':
                self.dlg.comboEmprise.setEnabled(False)
            else:
                # On remplit la combobox des departements
                self.dlg.comboEmprise.setEnabled(True)
                listEmprise = bbox.listEmprise
                self.cleEmprise = []
                for key in listEmprise:
                    for t in listEmprise[key]:
                        cle = key + "#" + t
                        self.cleEmprise.append(cle)
                        self.dlg.comboEmprise.addItem(key + " - " + listEmprise[key][t])
    
    def run_choucas(self):
        """
        Fonction qui permet d afficher les donnees voulues 
        en fonction du mode choisi (en ligne ou hors ligne)
        """
        
        if self.dlg.cb_fondcarte.isChecked():
            # On affiche un fond de carte de la France par défaut
            # S'il n'est pas déjà afficher
            estAffiche = False
            for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
                if lyr.name() == "France":
                    estAffiche = True
                    break            
            if not estAffiche :
                uri = os.path.join(os.path.dirname(__file__) + str('/resources/fond_de_carte/france/'),'France.shp')
                #fond_path = ':/plugins/PluginChoucas/fond_de_carte/France.shp'
                
                vlayer = QgsVectorLayer(uri, "France", "ogr")
                # symbol = QgsMarkerSymbolV2.createSimple({'name': '', 'color': 'land' })
                # vlayer.rendererV2().setSymbol(symbol)
                QgsMapLayerRegistry.instance().addMapLayer(vlayer) 
                
                
        # On recupere l'emprise selectionee
        selectedEmpriseIndex = self.dlg.comboEmprise.currentIndex()
        selectedEmprise = self.cleEmprise[selectedEmpriseIndex]
        tabCleEmprise = selectedEmprise.split("#")
        
        if self.dlg.comboEmprise.count() == 0:
            typeemprise = ''
            codeemprise = ''
        else:
            typeemprise = tabCleEmprise[0]
            codeemprise = tabCleEmprise[1]
        
        
        # On recupere la source selectionee
        selectedSourceIndex = self.dlg.comboSources.currentIndex()
        selectedSource = self.list_sources[selectedSourceIndex]
        self.source = selectedSource
        
        # On recupere l entite selectionee
        selectedEntityIndex = self.dlg.comboEntities.currentIndex()
        selectedEntity = self.list_entities[selectedEntityIndex]
        self.entity = selectedEntity
        
        # On definit le proxy
        util.chargeProxy(self.dlg.cb_proxy)
        
        # On calcule la bbox
        # Ecrins
        projection = util.get_first_object(self.root, self.source, 'projection')
        empriseSelect = util.get_first_object(self.root, self.source, 'emprise')
        # print ("emprise catalogue pour la source " + self.source + " = " + empriseSelect)
        if empriseSelect == 'none':
            card = None
        else:
            card = bbox.getBbox(typeemprise, codeemprise, projection)

        style = {}
        style['couleur'] = util.get_first_object(self.root, self.source, 'couleur')
        style['svg'] = util.get_second_object(self.root, self.source, self.entity, 'svg')
        style['size'] = util.get_second_object(self.root, self.source, self.entity, 'size')
        style['forme'] = util.get_second_object(self.root, self.source, self.entity, 'forme')
        
        typeGeom = util.get_second_object(self.root, self.source, self.entity, 'geom')
        urlQGis = typeGeom + '?crs=' + projection

        # Si le mode choisi est [En ligne]
        if self.dlg.rb_online.isChecked():
            
            # On recupere dans le catalogue 
            flux = util.get_first_object(self.root, self.source, 'flux')
            if flux == 'API':
                urlBrute = util.get_second_object(self.root, self.source, self.entity, 'url')
            else:
                urlBrute = ''
            
            attributs = util.get_attributs(self.root, self.source, self.entity)
            
            nomLayer = self.source + '-' + self.entity + '-' + codeemprise
            
            if self.source == 'osm':
                
                filtres = util.getFiltres(self.root, self.source, self.entity)
                osm.loadOSM(nomLayer, card, filtres, attributs, style)
                
            #    QMessageBox.information(None, "OUPS:", 
            #            'Departement non disponible pour cet API')
            else:
                if card == None:
                    url = urlBrute
                else:
                    # Par BBOX
                    url = online.getUrlWithBBox(card, urlBrute)
                # On ajoute la couche
                online.displayLayer(url, urlQGis, self.source, nomLayer, typeGeom, attributs, style)
        
        # Si le mode choisi est [Hors ligne]
        if self.dlg.rb_offline.isChecked():
            offline.offline(self.root, self.source, self.entity)
             
        if self.dlg.rb_local.isChecked():
            
            urlBrute = util.get_second_object(self.root, self.source, self.entity, 'url')
            nomLayer = self.source + '-' + self.entity + '-' + codeemprise
            # On prend tous les attribts quand c'est un fichier
            local.loadPoint(nomLayer, urlBrute, urlQGis, card, style)
            

    def onCloseMotClePlugin(self):
        """Cleanup necessary items here when plugin dlgMotCle is closed"""

        # disconnects
        #self.dlgMotCle.closingPlugin.disconnect(self.onCloseMotClePlugin)
        #self.pluginMotCleIsActive = False
        
        self.pluginMotCleIsActive = False
        self.dlgMotCle.close()

    def search(self):
        
        # print ("search")
        
        if not self.pluginMotCleIsActive:
            self.pluginMotCleIsActive = True       
       
            if self.dlgMotCle == None:
                self.dlgMotCle = RechercheMotcleDialog()
                
                # On peut charger les layers
                self.dlgMotCle.comboLayer.addItem("---")
                self.dlgMotCle.comboAttribut.addItem("---")
                
                layers = QgsMapLayerRegistry.instance().mapLayers().values()
                for layer in layers:
                    if layer.type() == QgsMapLayer.VectorLayer:
                        self.dlgMotCle.comboLayer.addItem(layer.name())

                # On connecte les listes déroulantes 
                self.dlgMotCle.comboLayer.currentIndexChanged.connect(self.fillAttr)
                
                # On connecte les boutons
                self.dlgMotCle.boutonCalculer.clicked.connect(self.doFiltre)
                self.dlgMotCle.boutonQuitter.clicked.connect(self.onCloseMotClePlugin)
                self.dlgMotCle.boutonRAZ.clicked.connect(self.razMotCle)
                
        #self.dlgMotCle.closingPlugin.connect(self.onCloseMotClePlugin)
       
        # show the dlgMotCle
        # TODO: fix to allow choice of dock location
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dlgMotCle)
        self.dlgMotCle.show()
        
        
    def fillAttr(self):
        self.dlgMotCle.comboAttribut.clear()
        
        nomLayer =  self.dlgMotCle.comboLayer.currentText()
        
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            nomAttributs = list()
            for field in layer.pendingFields():
                nomAttributs.append(field.name())
            nomAttributs.sort()
            # On remplit les listes correspondantes
            if layer.name() == nomLayer:
                for k in range (0, len (nomAttributs)):
                    # TODO : ne mettre que les attributs de type STRING
                    self.dlgMotCle.comboAttribut.addItem(nomAttributs[k])
    
    def razMotCle(self):
        self.dlgMotCle.comboLayer.clear()
        self.dlgMotCle.comboAttribut.clear()
        
        self.dlgMotCle.comboLayer.addItem("---")
        self.dlgMotCle.comboAttribut.addItem("---")
        
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                self.dlgMotCle.comboLayer.addItem(layer.name())
        
    def doFiltre(self):
        
        # On récupère : layer + attribut + mot clé
        nomLayer =  self.dlgMotCle.comboLayer.currentText()
        nomAttribut = self.dlgMotCle.comboAttribut.currentText()
        motCle = self.dlgMotCle.editMotCle.text()
        
        if nomLayer != '---' and nomAttribut != '---' and motCle != None and motCle != "":
            
            # On recupere le layer
            layers = QgsMapLayerRegistry.instance().mapLayers().values()
            for layer in layers:
                if layer.name() == nomLayer:
                    # On filtre
                    ancienFiltre = layer.subsetString()
                    if ancienFiltre != None and ancienFiltre != "":
                        filtreTxt = ancienFiltre + " and " + nomAttribut + " like '%" + motCle + "%' "
                    else:
                        filtreTxt = nomAttribut + " like '%" + motCle + "%' "
                    # print (filtreTxt)
                    layer.setSubsetString(filtreTxt)
                    # description like '%balcon%'
        
            # On ajoute le mot clé à la liste
            
    def displayDescription(self):
        
        print ("desc")
        #pluginDescriptionIsActive


