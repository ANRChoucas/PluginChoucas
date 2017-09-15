# -*- coding: utf-8 -*-

# =============================================================================
# http://rando.ecrins-parcnational.fr/fr/files/api/trek/938336/pois.geojson
# http://rando.ecrins-parcnational.fr/fr/files/api/trek/trek.geojson
#
# =============================================================================

from qgis.core import QgsVectorLayer
from qgis.core import QgsPoint, QgsGeometry, QgsFeature, QgsField
from PyQt4.QtCore import QVariant

import urllib2
import json


def loadItineraireVercors():
    
    url = 'http://rando.parc-du-vercors.fr/data/api/fr/treks.geojson'
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    print response.url
           
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