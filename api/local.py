# -*- coding: utf-8 -*-
"""
  Created on Jul 2017
  @author: Marie-Dominique
  
  Chargement de shapefiles
  
  TODO : transformer le texte en UTF-8
"""

from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsVectorLayer, QgsRectangle, QgsGeometry
# QgsVectorDataProvider
from qgis.core import QgsSvgMarkerSymbolLayerV2, QgsSymbolV2, QgsMarkerSymbolV2

import os


def loadPoint(nomLayer, urlLayer, urlQGis, card, style):
    
    vlayer = None
    memoryLayer = None
    uri = os.path.dirname(__file__) + str('/../resources/') + urlLayer
    vlayer = QgsVectorLayer(uri, nomLayer + "tmp", "ogr")
    
    # ------------------------------------------------------------------
    #  On intersecte avec l'emprise
    
    memoryLayer = QgsVectorLayer(urlQGis, nomLayer, "memory")
    pr = memoryLayer.dataProvider()

    # copy the table structure
    pr.addAttributes(vlayer.fields().toList())
    
    memoryLayer.updateFields()
    
    emprise = QgsRectangle(card[3], card[2], card[1], card[0])
    tabFeature = []
    for featPoint in vlayer.getFeatures():
        if QgsGeometry.fromRect(emprise).intersects(featPoint.geometry()):
            # vlayer.deleteFeature(featPoint.id())
            tabFeature.append(featPoint)
        
    pr.addFeatures(tabFeature)
    
    # On commit        
    memoryLayer.updateExtents()  
            
    # ------------------------------------------------------------------
    #  Symbolisation
    couleur = style['couleur']
    svg = style['svg']
    size = style['size']
    forme = style['forme']
    
    if svg == '':
        symbolLayer = QgsMarkerSymbolV2.createSimple({'name': str(forme), 'color': str(couleur)})
    else:
        svgStyle = {}
        filename = os.path.join(os.path.dirname(__file__) + str('/../resources/styles/'),  str(svg) +'_'+ str(couleur) + '.svg')
        svgStyle['size'] = size
        svgStyle['name'] = filename
        svgStyle['outline'] = '#000000'
        svgStyle['outline-width'] = '6.8'
        svgStyle['fill'] = '#00FFFF'
    
        symbolLayer = QgsSvgMarkerSymbolLayerV2.create(svgStyle)
    
    # symbolLayer.setPath(os.path.join(os.path.dirname(__file__) + str('/../resources/styles/'), str(svg) +'_'+ str(couleur) + '.svg'))
    symbol = QgsSymbolV2.defaultSymbol(memoryLayer.geometryType())
    symbol.changeSymbolLayer(0, symbolLayer)
    memoryLayer.rendererV2().setSymbol(symbol)
    
    memoryLayer.setCustomProperty("labeling", "pal")
    memoryLayer.setCustomProperty("labeling/enabled", "true")
    memoryLayer.setCustomProperty("labeling/fontFamily", "Arial")
    memoryLayer.setCustomProperty("labeling/fontSize", "9")
    memoryLayer.setCustomProperty("labeling/fieldName", "TOPONYME")
    memoryLayer.setCustomProperty("labeling/placement", "2")
    
    # ------------------------------------------------------------------
    #  On affiche
    QgsMapLayerRegistry.instance().addMapLayer(memoryLayer)


