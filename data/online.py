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
from qgis.core import QgsSvgMarkerSymbolLayerV2
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsPoint, QgsGeometry, QgsFeature, QgsField
from qgis.core import QgsMarkerSymbolV2
from PyQt4.QtCore import QVariant

import os

import util
import c2c

# =============================================================================
#
#
# =============================================================================
def online(root, list_dept, dept, source, type_pt, list_bbox, list_admin_area):
    """
        Fonction qui va interroger une api, recuperer les donnees en ligne et les afficher sous QGis
        dept: departement selectione
        source: source selectionnee
        type_pt: type d entites a afficher
    """
    # On cherche dans la liste de departement la position de celui qui a ete selectionne dans le plugin
    pos = list_dept.index(dept)
    # On recupere l attribut bbox (0 si fonctione par bbox, 1 si par limite administrative)
    bb = util.get_first_object(root, source,'bbox')
    if bb == '0':
        # On recupere dans la liste de bbox celle associee au departement choisi
        bbox = list_bbox[pos]
    elif bb == '1':
        # On recupere dans la liste des limites administratives celle associee au departement choisi
        bbox = list_admin_area[pos]

    # On recupere dans le catalogue le systeme dans lequel sont les donnees de l API source
    projection = util.get_first_object(root, source,'projection')
    # url associee au dpt, source et entite choisis
    url_temp = util.get_second_object(root, source,type_pt,'url')

    forme = util.get_second_object(root, source,type_pt,'forme')
    couleur = util.get_first_object(root, source,'couleur')

    # IGN cas particulier car flux WFS et non pas HTTP
    if source != 'IGN':
        # Si fonctionnement par bbox
        if bb == '0':
            url = url_temp+'&bbox='+bbox
            # Si fonctionnement par limites administratives
        elif bb == '1' :
            url = url_temp+';a='+bbox+';limit=100'
        else:
            url = url_temp

        # Appel au service + recuperation dans la variable data
        data = util.open_url(url)
        
        # Traitement supplementaire pour changer le json en Geojson
        if source == 'camptocamp':
            type_elem = util.get_second_object(root, source,type_pt,'type_elem')
            if int(data['total'])>100:
                data = c2c.iterate(url_temp,int(data['total']),data,bbox)
            data = c2c.parsage(data,type_elem)

        # geometrie de l entite
        geom = util.get_second_object(root, source,type_pt,'geom')
        # creation couche
        mem = geom+'?crs='+projection
        newLayer = QgsVectorLayer(mem, type_pt + '_' + source, "memory")
        # on recupere le fournisseur
        pr = newLayer.dataProvider()

        if geom == 'Point':
            # Donnees relatives a l element (symbole, taille symbole, attributs)
            svg = util.get_second_object(root, source,type_pt, 'svg')
            size_svg = util.get_second_object(root, source,type_pt, 'size')
            # TODO: Rendre cette partie plus generique (attributs inchangés selon la source)
            id_s = util.get_second_object(root, source,type_pt, 'id')
            nom_s = util.get_second_object(root, source,type_pt, 'nom')
            # ajoute les attributs au fournisseur
            pr.addAttributes([
                QgsField("id_0",  QVariant.Int),
                QgsField("nom", QVariant.String),
                QgsField("lat", QVariant.Int),
                QgsField("lon", QVariant.Int)
                #QgsField("alt", QVariant.Int)
            ])

            # On passe en mode edition
            newLayer.updateFields()
            # On boucle sur les features qu on a recu depuis la requete HTTP
            for point in data['features']:
                # Nouvel objet geo pour la couche
                ptfeature = QgsFeature()
                # la geometrie du point
                point1 = QgsPoint(float(point['geometry']['coordinates'][0]), float(point['geometry']['coordinates'][1]))
                pt = QgsGeometry.fromPoint(point1);
                ptfeature.setGeometry(pt)
                # On recupere les attributs dans le geojson
                id_0 = point[str(id_s)]
                nom = point['properties'][str(nom_s)]
                lat = point['geometry']['coordinates'][0]
                lon = point['geometry']['coordinates'][1]

                ptfeature.setAttributes([id_0, nom, lat, lon])

                # ajoute l objet au fournisseur
                pr.addFeatures([ptfeature])


            # Sauvegarde les changements
            newLayer.updateExtents()
            # On definitit le style de la couche
            if svg == '':
                symbol = QgsMarkerSymbolV2.createSimple({'name': str(forme), 'color': str(couleur)})
                newLayer.rendererV2().setSymbol(symbol)
            else:
                svgStyle = {}
                #svgStyle['fill'] = '#0000ff'
                svgStyle['fill'] = '#00FFFF'
                # Chemin ou se trouvent les styles
                # print os.path.join(os.path.dirname(__file__) + str('/../styles/'),  str(svg) +'_'+ str(couleur) + '.svg')
                filename = os.path.join(os.path.dirname(__file__) + str('/../styles/'),  str(svg) +'_'+ str(couleur) + '.svg')
                svgStyle['name'] = filename
                svgStyle['outline'] = '#000000'
                svgStyle['outline-width'] = '6.8'
                svgStyle['size'] = size_svg

                symbol = QgsSvgMarkerSymbolLayerV2.create(svgStyle)
                newLayer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol)

            if type_pt == 'lieux-dits':
                newLayer.setCustomProperty("labeling", "pal")
                newLayer.setCustomProperty("labeling/enabled", "true")
                newLayer.setCustomProperty("labeling/fontFamily", "Arial")
                newLayer.setCustomProperty("labeling/fontSize", "9")
                newLayer.setCustomProperty("labeling/fieldName", "nom")
                newLayer.setCustomProperty("labeling/placement", "2")

        elif geom == 'LineString':
            # Donnees relatives a l element (attributs)
            id_s = util.get_second_object(root, source, type_pt, 'id')

            # TODO: a rendre plus generique !
            nom_s = util.get_second_object(root, source,type_pt,'nom')
            description_s = util.get_second_object(root, source,type_pt,'description')

            # ajoute les attributs au fournisseur
            pr.addAttributes([
                QgsField("id_0",  QVariant.Int),
                QgsField("nom", QVariant.String),
                QgsField("description", QVariant.String)
            ])

            # On passe en mode edition
            newLayer.updateFields()

            # points = []
            # On boucle sur les features qu on a recu depuis la requete HTTP
            for point in data['features']:

                # points = []
                # Nouvel objet geo pour la couche
                ptfeature = QgsFeature()
                # la geometrie du point

                n = len(point['geometry']['coordinates'])
                typ = point['geometry']['type']
                # difference entre linestring et multi linestring
                if typ == 'LineString':
                # On recupere les premiers points
                    start_point = QgsPoint(float(point['geometry']['coordinates'][0][0]), float(point['geometry']['coordinates'][0][1]))
                    point_s = QgsPoint(float(point['geometry']['coordinates'][1][0]), float(point['geometry']['coordinates'][1][1]))
                    # On les relie
                    gLine = QgsGeometry.fromPolyline([start_point, point_s])
                    ptfeature.setGeometry(gLine)
                    # On ajoutes tous les autres points de la linestring
                    for i in range(1,n):
                        ptfeature = QgsFeature()
                        new_point = QgsPoint(float(point['geometry']['coordinates'][i][0]), float(point['geometry']['coordinates'][i][1]))
                        gLine = QgsGeometry.fromPolyline([point_s,new_point])
                        ptfeature.setGeometry(gLine)

                        id_0 = point[str(id_s)]
                        nom = point['properties'][str(nom_s)]
                        description = point['properties'][str(description_s)]

                        ptfeature.setAttributes([id_0, nom, description])

                        # ajoute l objet au fournisseur
                        pr.addFeatures([ptfeature])

                        newLayer.updateExtents()

                        point_s = new_point

        else:
            # flux WFS de l'IGN
            newLayer = QgsVectorLayer(url_temp, type_pt+'_'+source, "WFS")

        # La couche est creee, il faut l'ajouter a l'interface
        QgsMapLayerRegistry.instance().addMapLayer(newLayer)


