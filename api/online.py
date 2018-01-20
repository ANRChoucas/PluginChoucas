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

# =============================================================================
# Données issues du web
#
#
# =============================================================================

from qgis.core import QgsVectorLayer
from qgis.core import QgsSvgMarkerSymbolLayerV2, QgsLineSymbolV2
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsPoint, QgsGeometry, QgsFeature, QgsField
from qgis.core import QgsMarkerSymbolV2
from PyQt4.QtCore import QVariant

from HTMLParser import HTMLParser
import os

import util
import c2c

# =============================================================================
#   SI API
#   SINON WFS ???  ('IGN')
#
# typeGeom : Point ou LineString
# entity : refuge, sommet, etc.
#
# =============================================================================
def displayLayer(url, urlQGis, source, nomLayer, typeGeom, attributs, style):
    """
        Fonction qui va interroger une api, recuperer les donnees en ligne et les afficher sous QGis
        dept: departement selectione
        source: source selectionnee
        type_pt: type d entites a afficher
    """
    # Appel au service + recuperation dans la variable data
    data = util.open_url(url)
    # Traitement supplementaire pour changer le json en Geojson
    if source == 'camptocamp':
        if int(data['total']) > 30:
            data = c2c.iterate(url, int(data['total']), data)
        if typeGeom == 'Point':
            data = c2c.parsage(data, 'waypoints')
        elif typeGeom == 'LineString':
            data = c2c.parsage(data, 'routes')

    # creation couche
    newLayer = QgsVectorLayer(urlQGis, nomLayer, "memory")
    
    symbolisation = None
    if typeGeom == 'Point':
        buildLayerPoint(data, newLayer, attributs)
        symbolisation = buildStylePoint(style)
    # ligne
    if typeGeom == 'LineString':
        buildLayerLigne(data, newLayer, attributs)
        symbolisation = buildStyleLigne(style)
    #else:
        # flux WFS de l'IGN
        #newLayer = QgsVectorLayer(url_temp, type_pt+'_'+source, "WFS")
    
    # Sauvegarde les changements
    newLayer.updateExtents()  
    
    # Ajout du style
    # newLayer.rendererV2().setSymbol(symbolisation)
    if symbolisation != None:
        if type(symbolisation) == QgsSvgMarkerSymbolLayerV2:
            newLayer.rendererV2().symbols()[0].changeSymbolLayer(0, symbolisation)
        else:
            newLayer.rendererV2().setSymbol(symbolisation)
    
    # La couche est creee, il faut l'ajouter a l'interface
    QgsMapLayerRegistry.instance().addMapLayer(newLayer)



def getUrlWithBBox(card, url):
    
    # (north, east, south, west)
    # bbox=5.5,45.1,6.5,45.6
    # print (card)
    bbox = str(card[3]) + "," + str(card[2]) + "," + str(card[1]) + "," + str(card[0])
    urlComplete = url + '&bbox=' + bbox
    # print(urlComplete)
    return urlComplete



def buildLayerPoint(data, newLayer, attributs):
    
    # TODO: Rendre cette partie plus generique (attributs inchangés selon la source)
    
    # on recupere le fournisseur
    pr = newLayer.dataProvider()
    
    attributeList = []
    for attr in attributs:
        if attributs[attr]['type'] == 'string':
            attributeList.append(QgsField(attr,  QVariant.String))
        if attributs[attr]['type'] == 'int':
            attributeList.append(QgsField(attr,  QVariant.Int))
        if attributs[attr]['type'] == 'double':
            attributeList.append(QgsField(attr,  QVariant.Double))
    pr.addAttributes(attributeList)
    # ajoute les attributs au fournisseur
    #pr.addAttributes([
    #    QgsField("id",  QVariant.String),
    #    QgsField("nom", QVariant.String)
    #])
    
    for field in newLayer.pendingFields():
        print ("attr:" + field.name() + "," + field.typeName())
    
    # On passe en mode edition
    newLayer.updateFields()

    # On boucle sur les features qu on a recu depuis la requete HTTP
    for point in data['features']:
        # Nouvel objet geo pour la couche
        ptfeature = QgsFeature()
        
        # la geometrie du point
        geomPoint = QgsPoint(float(point['geometry']['coordinates'][0]), float(point['geometry']['coordinates'][1]))
        pt = QgsGeometry.fromPoint(geomPoint);
        ptfeature.setGeometry(pt)
        
        # On recupere les attributs dans le geojson
        attrFeature = []
        for attr in attributs:
            chemin = attributs[attr]['chemin']
            tabchemin = chemin.split(",")
            if len(tabchemin) == 1:
                #print(chemin + '---' + str(point['properties']['qualite']))
                attrFeature.append(point[tabchemin[0]])
            elif len(tabchemin) == 2:
                attVal = point[tabchemin[0]][tabchemin[1]]
                attrFeature.append(attVal)
            elif len(tabchemin) == 3:
                attrFeature.append(point[tabchemin[0]][tabchemin[1]][tabchemin[2]])
        # On ajoute les attributs au feature
        ptfeature.setAttributes(attrFeature)
        
        # ajoute l objet au fournisseur
        pr.addFeatures([ptfeature])


            
def buildStylePoint(style):
    
    couleur = style['couleur']
    svg = style['svg']
    size = style['size']
    forme = style['forme']
    
    # On definitit le style de la couche
    if svg == 'none':
        symbol = QgsMarkerSymbolV2.createSimple({'name': str(forme), 'color': str(couleur)})
    else:
        svgStyle = {}
        svgStyle['fill'] = '#00FFFF'
        # Chemin ou se trouvent les styles
        filename = os.path.join(os.path.dirname(__file__) + str('/../resources/styles/'),  str(svg) +'_'+ str(couleur) + '.svg')
        svgStyle['name'] = filename
        svgStyle['outline'] = '#000000'
        svgStyle['outline-width'] = '6.8'
        svgStyle['size'] = size

        symbol = QgsSvgMarkerSymbolLayerV2.create(svgStyle)
    
    return symbol

#    if type_pt == 'lieux-dits':
#        newLayer.setCustomProperty("labeling", "pal")
#        newLayer.setCustomProperty("labeling/enabled", "true")
#        newLayer.setCustomProperty("labeling/fontFamily", "Arial")
#        newLayer.setCustomProperty("labeling/fontSize", "9")
#        newLayer.setCustomProperty("labeling/fieldName", "nom")
#        newLayer.setCustomProperty("labeling/placement", "2")

def buildStyleLigne(style):
    
    couleur = style['couleur']
    size = style['size']
    
    symbolL = QgsLineSymbolV2.createSimple({'penstyle':'solid', 'width':size, 'color': str(couleur)})
    return symbolL

    
def buildLayerLigne(data, newLayer, attributs):
    
    # TODO: Rendre cette partie plus generique (attributs inchangés selon la source)
    
    # on recupere le fournisseur
    pr = newLayer.dataProvider()
    
    # ajoute les attributs au fournisseur
    attributeList = []
    for attr in attributs:
        if attributs[attr]['type'] == 'string':
            attributeList.append(QgsField(attr,  QVariant.String))
        if attributs[attr]['type'] == 'int':
            attributeList.append(QgsField(attr,  QVariant.Int))
        if attributs[attr]['type'] == 'double':
            attributeList.append(QgsField(attr,  QVariant.Double))
    pr.addAttributes(attributeList)

    
    # On passe en mode edition
    newLayer.updateFields()
    
    # points = []
    # On boucle sur les features qu on a recu depuis la requete HTTP
    cptNonAttribue = 0
    for point in data['features']:

        if point['geometry'] != '--':
            # la geometrie du point
            n = len(point['geometry']['coordinates'])
            typ = point['geometry']['type']
            
            # difference entre linestring et multi linestring
            points = []
            if typ == 'LineString':
                for i in range(0, n):
                    x = float(point['geometry']['coordinates'][i][0])
                    y = float(point['geometry']['coordinates'][i][1])
                    pt = QgsPoint(x, y)
                    points.append(pt)
                if len(points) > 1:
                    
                    # Nouvel objet geo pour la couche
                    ptfeature = QgsFeature()
                    ptfeature.setGeometry(QgsGeometry.fromPolyline(points))
    
                    #idf = str(point['id'])
                    #nom = point['properties']['nom']
                    # print(nom + str(len(points)))
                    #description = point['properties'][str(description_s)]
                    #ptfeature.setAttributes([idf, nom])
                    
                    # On recupere les attributs dans le geojson
                    attrFeature = []
                    for attr in attributs:
                        chemin = attributs[attr]['chemin']
                        tabchemin = chemin.split(",")
                        if len(tabchemin) == 1:
                            #print(chemin + '---' + str(point['properties']['qualite']))
                            attrFeature.append(point[tabchemin[0]])
                        elif len(tabchemin) == 2:
                            attVal = point[tabchemin[0]][tabchemin[1]]
                            if attVal != None and attVal != '':
                                if attributs[attr]['name'] == 'description':
                                    h = HTMLParser()
                                    attVal = h.unescape(attVal)
                            attrFeature.append(attVal)
                            # attrFeature.append(point[tabchemin[0]][tabchemin[1]])
                        elif len(tabchemin) == 3:
                            attrFeature.append(point[tabchemin[0]][tabchemin[1]][tabchemin[2]])
                    ptfeature.setAttributes(attrFeature)
                    
                    # ajoute l objet au fournisseur
                    pr.addFeatures([ptfeature])
            else:
                print("multiligne " + typ)
                # print(point['geometry'])
            
            # Set geometry
        else:
            cptNonAttribue = cptNonAttribue + 1
            
    print("Nb sans geometrie = " + str(cptNonAttribue))

                
