# -*- coding: utf-8 -*-

# =============================================================================
# http://rando.ecrins-parcnational.fr/fr/files/api/trek/938336/pois.geojson
# http://rando.ecrins-parcnational.fr/fr/files/api/trek/trek.geojson
#
# =============================================================================

from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsVectorLayer
from qgis.core import QgsPoint, QgsGeometry, QgsFeature, QgsField
from qgis.core import QgsSvgMarkerSymbolLayerV2, QgsSymbolV2, QgsMarkerSymbolV2
from PyQt4.QtCore import QVariant

import urllib2
import json


def loadPointEcrin(style):
    
    url = 'http://rando.ecrins-parcnational.fr/fr/files/api/trek/trek.geojson'
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    
    vl = QgsVectorLayer("Point?crs=epsg:4326", "Points Ecrins", "memory")
    pr = vl.dataProvider()
           
    # add fields
    pr.addAttributes([
        QgsField("id",  QVariant.Int),
        QgsField("type",  QVariant.String),
        QgsField("nom",  QVariant.String),
        QgsField("altitude",  QVariant.Int)
    ])
           
    vl.updateFields()
           
    data = json.load(response)
    
    for ligne in data['features']:
        id = ligne['id']
        urlPoint = 'http://rando.ecrins-parcnational.fr/fr/files/api/trek/' + str(id) + '/pois.geojson'
        requestPoint = urllib2.Request(urlPoint)
        responsePoint = urllib2.urlopen(requestPoint)
        
        dataPoint = json.load(responsePoint)
        for point in dataPoint['features']:
            
            # Nouvel objet geo pour la couche
            ptfeature = QgsFeature()
            
            attrFeature = []
            id = point['id']
            attrFeature.append(id)
            type = point['properties']['type']['label']
            attrFeature.append(type)
            nom = point['properties']['name']
            attrFeature.append(nom)
            ele = point['properties']['elevation']
            attrFeature.append(ele)
            ptfeature.setAttributes(attrFeature)
            
            # la geometrie du point
            xPoint = float(point['geometry']['coordinates'][0])
            yPoint = float(point['geometry']['coordinates'][1])
            geomPoint = QgsPoint(xPoint, yPoint)
            pt = QgsGeometry.fromPoint(geomPoint);
            ptfeature.setGeometry(pt)
            
            pr.addFeatures([ptfeature])
            
    vl.updateExtents()
    
    #  Symbolisation
    couleur = style['couleur']
    size = style['size']
    forme = style['forme']
    
    symbolLayer = QgsMarkerSymbolV2.createSimple({'name': str(forme), 'color': str(couleur)})
    vl.rendererV2().setSymbol(symbolLayer)
        
    QgsMapLayerRegistry.instance().addMapLayer(vl)


def loadItineraireVercors():
    
    url = 'http://rando.parc-du-vercors.fr/data/api/fr/treks.geojson'
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    print (response.url)
           
    data = json.load(response)
    #print data['generator']
           
    vl = QgsVectorLayer("Linestring?crs=epsg:4326", "Iti Vercors", "memory")
    pr = vl.dataProvider()
           
    # add fields
    pr.addAttributes([
        QgsField("id",  QVariant.Int),
        QgsField("type",  QVariant.String),
        QgsField("depart",  QVariant.String),
        QgsField("arrivee",  QVariant.String),
        QgsField("duree",  QVariant.Double),
        QgsField("nom",  QVariant.String),
        QgsField("difficulte",  QVariant.Int),
        QgsField("usage",  QVariant.String),
    ])
           
    vl.updateFields()
           
    for ligne in data['features']:
        typeGeom =  ligne['geometry']['type']
                
        depart = ligne['properties']['departure']
        arrivee = ligne['properties']['arrival']
        duree = ligne['properties']['duration']
        nom = ligne['properties']['name']
        difficulte = ligne['properties']['difficulty']['label']
        usage = ligne['properties']['usages'][0]['label']
                
                
        if typeGeom == 'LineString':
            ptfeature = QgsFeature()
                    
            # la géométrie du point
            coordpoly = ligne['geometry']['coordinates']
            n = len(coordpoly)
            #print n
                   
            points = []
            for e in range(0, n):
                pt = QgsPoint(coordpoly[e][0], coordpoly[e][1])
                points.append(pt)
            ptfeature.setGeometry(QgsGeometry.fromPolyline(points))
                   
            id = ligne['id']
            # print id
            ptfeature.setAttributes([id, 'linestring', depart, arrivee, duree, nom, difficulte, usage])
                    
            pr.addFeatures([ptfeature])
                
        elif typeGeom == 'MultiLineString':                
                    
            # On récupère les lignes
            listeLigne =  ligne['geometry']['coordinates']
            nligne = len(listeLigne)
            for l in range(0, nligne):
                coordpoly = listeLigne[l]
                n = len(coordpoly)
                        
                ptfeature = QgsFeature()
                points = []
                for e in range(0, n):
                    pt = QgsPoint(coordpoly[e][0], coordpoly[e][1])
                    points.append(pt)
                ptfeature.setGeometry(QgsGeometry.fromPolyline(points))
                       
                id = ligne['id']
                # print id
                ptfeature.setAttributes([id, 'multilinestring', depart, arrivee, duree, nom, difficulte, usage])
                        
                pr.addFeatures([ptfeature])
                    
        else:
            print typeGeom
                
    
    vl.updateExtents()
    return vl
    
    
def loadItineraireVanoise():
    
    url = 'http://rando.vanoise.com/data/api/fr/treks.geojson'
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    # print response.url
           
    data = json.load(response)
    #print data['generator']
           
    vl = QgsVectorLayer("Linestring?crs=epsg:4326", "Iti Vanoise", "memory")
    pr = vl.dataProvider()
           
    # add fields
    pr.addAttributes([
        QgsField("id",  QVariant.Int),
        QgsField("type",  QVariant.String),
        QgsField("depart",  QVariant.String),
        QgsField("arrivee",  QVariant.String),
        QgsField("duree",  QVariant.Double),
        QgsField("nom",  QVariant.String),
        QgsField("difficulte",  QVariant.Int),
        QgsField("usage",  QVariant.String),
    ])
           
    vl.updateFields()
           
    for ligne in data['features']:
        typeGeom =  ligne['geometry']['type']
                
        depart = ligne['properties']['departure']
        arrivee = ligne['properties']['arrival']
        duree = ligne['properties']['duration']
        nom = ligne['properties']['name']
        difficulte = ligne['properties']['difficulty']['label']
        usage = ligne['properties']['usages'][0]['label']
                
                
        if typeGeom == 'LineString':
            
            ptfeature = QgsFeature()
                    
            # la géométrie du point
            coordpoly = ligne['geometry']['coordinates']
            n = len(coordpoly)
            #print n
                   
            points = []
            for e in range(0, n):
                pt = QgsPoint(coordpoly[e][0], coordpoly[e][1])
                points.append(pt)
            ptfeature.setGeometry(QgsGeometry.fromPolyline(points))
                   
            id = ligne['id']
            # print id
            ptfeature.setAttributes([id, 'linestring', depart, arrivee, duree, nom, difficulte, usage])
                    
            pr.addFeatures([ptfeature])
                
        elif typeGeom == 'MultiLineString':                
                    
            # On récupère les lignes
            listeLigne =  ligne['geometry']['coordinates']
            nligne = len(listeLigne)
            for l in range(0, nligne):
                coordpoly = listeLigne[l]
                n = len(coordpoly)
                        
                ptfeature = QgsFeature()
                points = []
                for e in range(0, n):
                    pt = QgsPoint(coordpoly[e][0], coordpoly[e][1])
                    points.append(pt)
                ptfeature.setGeometry(QgsGeometry.fromPolyline(points))
                       
                id = ligne['id']
                # print id
                ptfeature.setAttributes([id, 'multilinestring', depart, arrivee, duree, nom, difficulte, usage])
                        
                pr.addFeatures([ptfeature])
                    
        else:
            
            print typeGeom
                
    
    vl.updateExtents()
    return vl
    
    
def loadItineraireEcrin():
    
    url = 'http://rando.ecrins-parcnational.fr/fr/files/api/trek/trek.geojson'
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    # print response.url
           
    data = json.load(response)
    #print data['generator']
           
    vl = QgsVectorLayer("Linestring?crs=epsg:4326", "Iti Ecrin", "memory")
    pr = vl.dataProvider()
           
    # add fields
    pr.addAttributes([
        QgsField("id",  QVariant.Int),
        QgsField("type",  QVariant.String),
        QgsField("depart",  QVariant.String),
        QgsField("arrivee",  QVariant.String),
        QgsField("duree",  QVariant.Double),
        QgsField("nom",  QVariant.String),
        QgsField("difficulte",  QVariant.Int),
        QgsField("usage",  QVariant.String),
    ])
           
    vl.updateFields()
           
    for ligne in data['features']:
        typeGeom =  ligne['geometry']['type']
                
        depart = ligne['properties']['departure']
        arrivee = ligne['properties']['arrival']
        duree = ligne['properties']['duration']
        nom = ligne['properties']['name']
        difficulte = ligne['properties']['difficulty']['label']
        usage = ligne['properties']['usages'][0]['label']
                
                
        if typeGeom == 'LineString':
            
            ptfeature = QgsFeature()
                    
            # la géométrie du point
            coordpoly = ligne['geometry']['coordinates']
            n = len(coordpoly)
            #print n
                   
            points = []
            for e in range(0, n):
                pt = QgsPoint(coordpoly[e][0], coordpoly[e][1])
                points.append(pt)
            ptfeature.setGeometry(QgsGeometry.fromPolyline(points))
                   
            id = ligne['id']
            # print id
            ptfeature.setAttributes([id, 'linestring', depart, arrivee, duree, nom, difficulte, usage])
                    
            pr.addFeatures([ptfeature])
                
        elif typeGeom == 'MultiLineString':                
                    
            # On récupère les lignes
            listeLigne =  ligne['geometry']['coordinates']
            nligne = len(listeLigne)
            for l in range(0, nligne):
                coordpoly = listeLigne[l]
                n = len(coordpoly)
                        
                ptfeature = QgsFeature()
                points = []
                for e in range(0, n):
                    pt = QgsPoint(coordpoly[e][0], coordpoly[e][1])
                    points.append(pt)
                ptfeature.setGeometry(QgsGeometry.fromPolyline(points))
                       
                id = ligne['id']
                # print id
                ptfeature.setAttributes([id, 'multilinestring', depart, arrivee, duree, nom, difficulte, usage])
                        
                pr.addFeatures([ptfeature])
                    
        else:
            
            print typeGeom
                
    
    vl.updateExtents()
    return vl