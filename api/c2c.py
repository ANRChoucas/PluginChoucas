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
# Données de C2C, ...
#
#
# =============================================================================

import json
import util


def detailRoute(document_id):
    """
        Effectue des requetes à partir de l'ID
    """
    url = 'https://api.camptocamp.org/routes/' + str(document_id)
    # print(url)
    dataDetailRoute = util.open_url(url)
    return dataDetailRoute

    
def parsage(data, type_request):
    """
        data : variable dictionnaire (json) renvoyée par la fonction 'client_search'
        type_request : waypoints OU routes

        Fonction qui parse le json renvoyé par l'API C2C en 'geojson'
    """
    
    # Résultat parsé
    result_json = None
    # Liste vide permettant la concaténation des éléments au format convenable
    wp, r = [], []
    
    # Parcourt le fichier data
    for i in range(len(data["documents"])): 
        
        feature = data['documents'][i]
        idfeature = feature["document_id"] # Récupère l'id
        
        #Selon ce qu'on cherche, la strucutre du JSON varie
        if type_request == 'waypoints':
            geom = json.loads(feature['geometry']['geom']) # Récupère la géométrie
            lon = geom["coordinates"][0]
            lat = geom["coordinates"][1]
            # Concaténation de la liste au format GeoJson
            info = {}
            info['type'] = 'Feature'
            info['id'] = idfeature
            prop = {}
            prop['id'] = idfeature
            prop['coord'] = {'long' : lon, 'lat' : lat,}
            prop['nom'] = feature["locales"][0]['title']
            prop['altitude'] = feature["elevation"]
            prop['type'] = feature["waypoint_type"]
            prop['qualite'] = feature["quality"]
            info['properties'] = prop
            info['geometry'] = geom
            wp.append (info)
        elif type_request == 'routes':
            # Concaténation de la liste au format GeoJson
            info = {}
            info['type'] = 'Feature'
            info['id'] = idfeature
            prop = {}
            prop['id'] = idfeature
            prop['nom'] = feature["locales"][0]['title']
            if "hiking_rating" in feature:
                prop['hiking_rating'] = feature["hiking_rating"]
            else:
                prop['hiking_rating'] = ""
            # prop['coord'] = {'long' : lon, 'lat' : lat}
            if "elevation_max" in feature:
                prop['altitude_max'] = feature["elevation_max"]
            else:
                prop['altitude_max'] = ""
            if "height_diff_up" in feature:
                prop['height_diff_up'] = feature["height_diff_up"]
            else:
                prop['height_diff_up'] = ""
            if "quality" in feature:
                prop['quality'] = feature["quality"]
            else:
                prop['quality'] = ""
            
            #info['geometry'] = geom

            # Appel au web service pour le détail de la route
            trace_route = detailRoute(idfeature) 
            # Attribut "description" de la route
            prop['description'] = trace_route['locales'][0]['description'] 
            info['properties'] = prop
            # Géométrie
            geom2 = trace_route['geometry']['geom_detail'] # Géométrie de la polyligne correspondant au tracé GPS
            if geom2 != None:
                info['geometry'] = json.loads(geom2)
            else:
                info['geometry'] = '--'
            
            r.append (info)
    
    if type_request=='waypoints':
        result_json = wp
    elif type_request=='routes':
        result_json = r
    
    resultat = {'type': 'FeatureCollection', 'features': result_json}
    return resultat


def iterate(url, total, data):
    """
        Effectue une boucle pour concaténer les différentes requetes 
        (limite de 30 résultats par requete)
    """
    
    nbiter = total / 30 + 1
    offset = 30
    for j in range (1, nbiter):
        url = url + '&offset=' + str(offset)
        datasup = util.open_url(url)
        data['documents'] += datasup['documents']
        offset = offset + 30
    
    return data