# -*- coding: utf-8 -*-
"""
Created on 2017-07

@author: Marie-Dominique
"""

import os
from qgis.core import QgsVectorLayer, QgsPoint
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform
# QgsMapLayerRegistry

listEmprise = {}

listEmprise["pn"] = {}
listEmprise["pn"]["Cevennes"] = "Cevennes"
listEmprise["pn"]["Ecrins"] = "Ecrins"
listEmprise["pn"]["Mercantour"] = "Mercantour"
listEmprise["pn"]["Vanoise"] = "Vanoise"

listEmprise["dep"] = {}
# listEmprise["dep"]["01"] = "Ain"
# listEmprise["dep"]["07"] = "Ardeche"
listEmprise["dep"]["26"] = "Drome"
listEmprise["dep"]["05"] = "Hautes-Alpes"
listEmprise["dep"]["38"] = "Isere"
# listEmprise["dep"]["42"] = "Loire"
# listEmprise["dep"]["69"] = "Rhone"
listEmprise["dep"]["73"] = "Savoie"
listEmprise["dep"]["74"] = "Haute-savoie"

listEmprise["massifs"] = {}
listEmprise["massifs"]["zoneetude"] = "Zone-Etude"

# list_pnr = ['Chartreuse', 'Massif des Bauges, Vercors', 'Queyras', 'Verdon']

# Liste des limites administratives
# list_admin_area = ['14370', '14359', '14342', '14328', '14325', '14299', '14295', '14366']


"""
  Retourne l'emprise sous la forme d'une bbox en coordonnées 4326
"""
def getBbox(typeEmprise, valEmprise, crsSource):
    
    cheminRelatif = str('/../resources/fond_de_carte/emprise_' + typeEmprise + '/')
    nomFichier = typeEmprise + '_' + valEmprise + '.shp'
    # print(nomFichier)
    uri = os.path.join(os.path.dirname(__file__) + cheminRelatif, nomFichier)
    pnlayer = QgsVectorLayer(uri, valEmprise, "ogr")
    rect = pnlayer.extent() 
        
    sourceCrs = QgsCoordinateReferenceSystem("EPSG:2154")
    targetCrs = QgsCoordinateReferenceSystem(crsSource)
    tr = QgsCoordinateTransform(sourceCrs, targetCrs)
        
    pt1 = tr.transform(QgsPoint(rect.xMinimum(), rect.yMinimum()))
    pt2 = tr.transform(QgsPoint(rect.xMaximum(), rect.yMaximum()))
    north = pt2.y()
    south = pt1.y()
    east = pt2.x()
    west = pt1.x()
        
    card = (north, east, south, west)
    # print(card)
    return card

