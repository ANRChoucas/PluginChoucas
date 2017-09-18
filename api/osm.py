# -*- coding: utf-8 -*-
"""
Created on 2017-07
@author: Marie-Dominique Van Damme

"""

# ===================================================================================
# online.py:162: DeprecationWarning: QgsFeatureRendererV2.symbols() is deprecated
# 
#  bbox ??
#
#

from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsVectorLayer
from qgis.core import QgsPoint, QgsGeometry, QgsFeature, QgsField
from qgis.core import QgsSvgMarkerSymbolLayerV2, QgsSymbolV2, QgsMarkerSymbolV2
from PyQt4.QtCore import QVariant

import os

import urllib
import urllib2
import xml.etree.cElementTree as ET

# --------------------------------------------------------------------------
#  tourism 	: alpine_hut, wilderness_hut 
#
def loadOSM(nomLayer, card, filtres, attributs, style):
    
    north = card[0] # "45.7896"
    south = card[2] # "44.9852"
    east  = card[1] # "7.5462"
    west  = card[3] # "5.7198"
    
    # -------------------------------------------------------------------
    #  Appel au service web
    
    dataReqNode = ""
    dataReqWay = ""
    dataReqRelation = ""
    for cleval in filtres:
        cle = cleval.split('#')[0]
        featureType = cleval.split('#')[1] #filtres[cle]['valeur']
        typeTag = filtres[cleval]
        
        # print (typeTag + '-' + cle + "-" + featureType)
        
        if typeTag == 'node':
            dataReqNode = dataReqNode + "<query type=\"node\">"
            dataReqNode = dataReqNode + "<has-kv k=\"" + cle + "\" v=\"" + featureType + "\" />"
            dataReqNode = dataReqNode + "<bbox-query "
            dataReqNode = dataReqNode + "e=\"" + str(east) + "\" "
            dataReqNode = dataReqNode + "n=\"" + str(north) + "\" " 
            dataReqNode = dataReqNode + "s=\"" + str(south) + "\" " 
            dataReqNode = dataReqNode + "w=\"" + str(west) + "\" />"
            dataReqNode = dataReqNode + "</query>"
            
            dataReqWay = dataReqWay + "<query type=\"way\">"
            dataReqWay = dataReqWay + "<has-kv k=\"" + cle + "\" v=\"" + featureType + "\" />"
            dataReqWay = dataReqWay + "<bbox-query "
            dataReqWay = dataReqWay + "e=\"" + str(east) + "\" "
            dataReqWay = dataReqWay + "n=\"" + str(north) + "\" " 
            dataReqWay = dataReqWay + "s=\"" + str(south) + "\" " 
            dataReqWay = dataReqWay + "w=\"" + str(west) + "\" />"
            dataReqWay = dataReqWay + "</query>"
            
            dataReqRelation = dataReqRelation + "<query type=\"relation\">"
            dataReqRelation = dataReqRelation + "<has-kv k=\"" + cle + "\" v=\"" + featureType + "\" />"
            dataReqRelation = dataReqRelation + "<bbox-query "
            dataReqRelation = dataReqRelation + "e=\"" + str(east) + "\" "
            dataReqRelation = dataReqRelation + "n=\"" + str(north) + "\" " 
            dataReqRelation = dataReqRelation + "s=\"" + str(south) + "\" " 
            dataReqRelation = dataReqRelation + "w=\"" + str(west) + "\" />"
            dataReqRelation = dataReqRelation + "</query>"
            
            
        # 
    dataRequest = "<osm-script>"
    dataRequest = dataRequest + "<union into=\"_\">"
    
    # Plus les noeuds
    dataRequest = dataRequest + dataReqNode
    # Plus les ways
    dataRequest = dataRequest + dataReqWay
    # Plus les relations
    dataRequest = dataRequest + dataReqRelation
    
    dataRequest = dataRequest + "</union>"
    dataRequest = dataRequest + "<union>"
    dataRequest = dataRequest + "<item/>"
    dataRequest = dataRequest + "<recurse type=\"down\"/>"
    dataRequest = dataRequest + "</union>"
    dataRequest = dataRequest + "<print mode=\"meta\"/>"
    dataRequest = dataRequest + "</osm-script>"
    
    # print(dataRequest)
    
    http = 'http://overpass.osm.rambler.ru/cgi/interpreter?'
    #http = 'http://overpass-api.de/api/interpreter?'
    
    dataRequest = dataRequest.encode('utf8')
    query_string = urllib.urlencode({'data': dataRequest})    
    data = urllib2.urlopen(url=http, data=query_string).read()
    # print(data)
    root = ET.fromstring(data)
    
    # -----------------------------------------------------------------------
    #   POINT
    
    # Traitement des données de type point
    allnodes = root.findall('node')
    if (len(allnodes) > 1):
    
        # Creation du layer point
        vl1 = QgsVectorLayer("Point?crs=epsg:4326", nomLayer, "memory")
        pr1 = vl1.dataProvider()
        
        attributeList = []
        attributeList.append(QgsField("id",  QVariant.String))
        for attr in attributs:
            if attributs[attr]['type'] == 'string':
                attributeList.append(QgsField(attr,  QVariant.String))
            if attributs[attr]['type'] == 'int':
                attributeList.append(QgsField(attr,  QVariant.Int))
            if attributs[attr]['type'] == 'double':
                attributeList.append(QgsField(attr,  QVariant.Double))
        pr1.addAttributes(attributeList)
                   
        vl1.updateFields()
        
        for node in allnodes:
            lat = node.get('lat')
            lon = node.get('lon')
            nodeid = node.get('id')
            
            valAttr = {}
            isFeature = False
            for attr in attributs:
                valAttr[attr] = ""
            for tag in node.findall('tag'):
                for attr in attributs:
                    if attributs[attr]['chemin'] == tag.get('k'):
                        # print (attributs[attr]['chemin'] + "#" + tag.get('k'))
                        valAttr[attr] = tag.get('v')
                for cleval in filtres:
                    cle = cleval.split('#')[0]
                    if cle == tag.get('k'):
                        isFeature = True
                
            if isFeature:
                ptfeature1 = QgsFeature()
                    
                point1 = QgsPoint(float(lon), float(lat))
                pt = QgsGeometry.fromPoint(point1);
                ptfeature1.setGeometry(pt)
                    
                ptfeature1.setAttributes([nodeid] + valAttr.values())
                pr1.addFeatures([ptfeature1])
        
        vl1.updateExtents()   
        
        #  Symbolisation
        couleur = style['couleur']
        svg = style['svg']
        size = style['size']
        forme = style['forme']
        
        if svg == '':
            symbolLayer = QgsMarkerSymbolV2.createSimple({'name': str(forme), 'color': str(couleur)})
        else:
            svgStyle = {}
            svgStyle['fill'] = '#00FFFF'
            # Chemin ou se trouvent les styles
            filename = os.path.join(os.path.dirname(__file__) + str('/../resources/styles/'),  str(svg) +'_'+ str(couleur) + '.svg')
            svgStyle['name'] = filename
            svgStyle['outline'] = '#000000'
            svgStyle['outline-width'] = '6.8'
            svgStyle['size'] = size

            symbolLayer = QgsSvgMarkerSymbolLayerV2.create(svgStyle)
    
        symbol = QgsSymbolV2.defaultSymbol(vl1.geometryType())
        symbol.changeSymbolLayer(0, symbolLayer)
        vl1.rendererV2().setSymbol(symbol)
        
        vl1.setCustomProperty("labeling", "pal")
        vl1.setCustomProperty("labeling/enabled", "true")
        vl1.setCustomProperty("labeling/fontFamily", "Arial")
        vl1.setCustomProperty("labeling/fontSize", "9")
        vl1.setCustomProperty("labeling/fieldName", "nom")
        vl1.setCustomProperty("labeling/placement", "2")
        
        QgsMapLayerRegistry.instance().addMapLayer(vl1)
    
    
    # -----------------------------------------------------------------------
    #   WAY
    
    # Traitement des données de type ligne
    
    allways = root.findall('way')
    if (len(allways) > 1):
    
        # Creation du layer ligne
        vl2 = QgsVectorLayer("Polygon?crs=epsg:4326", nomLayer, "memory")
        pr2 = vl2.dataProvider()
        
        attributeList = []
        attributeList.append(QgsField("id",  QVariant.String))
        for attr in attributs:
            if attributs[attr]['type'] == 'string':
                attributeList.append(QgsField(attr,  QVariant.String))
            if attributs[attr]['type'] == 'int':
                attributeList.append(QgsField(attr,  QVariant.Int))
            if attributs[attr]['type'] == 'double':
                attributeList.append(QgsField(attr,  QVariant.Double))
        pr2.addAttributes(attributeList)
                   
        vl2.updateFields()
    
        for way in allways:
            
            wayid = way.get('id')
            
            # Attributs
            valAttr = {}
            for attr in attributs:
                valAttr[attr] = ""
            for tag in way.findall('tag'):
                for attr in attributs:
                    if attributs[attr]['chemin'] == tag.get('k'):
                        # print (attributs[attr]['chemin'] + "#" + tag.get('k'))
                        valAttr[attr] = tag.get('v')
        
            # Géométrie
            vertices = []
            for node in way.findall('nd'):
                ref = node.get('ref')
                for vertex in allnodes:
                    if vertex.get('id') == ref:
                        # vertices.append(vertex)
                        pt = QgsPoint(float(vertex.get('lon')), float(vertex.get('lat')))
                        vertices.append(pt)
            # print ("nb vertex de la ligne = " + str(len(vertices)))
            
            ptfeature2 = QgsFeature()
            geomEnv = QgsGeometry.fromPolygon([vertices])
            ptfeature2.setGeometry(geomEnv)
                    
            ptfeature2.setAttributes([wayid] + valAttr.values())
            pr2.addFeatures([ptfeature2])
        
        vl2.updateExtents() 
        
        # Symbolisation
        
        
        # On ajoute au panneau
        QgsMapLayerRegistry.instance().addMapLayer(vl2)
        
    
    # -----------------------------------------------------------------------
    #   RELATION
    
    # Traitement des données de type relation
    allrelations = root.findall('relation')
    
    
    
    # -----------------------------------------------------------------------
    print ("Nb noeud = " + str(len(allnodes)))
    print ("Nb ligne = " + str(len(allways)))
    print ("Nb relation = " + str(len(allrelations)))
    
    
    