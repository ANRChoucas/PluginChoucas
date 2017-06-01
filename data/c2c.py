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


def route(document_id):
    """
        Effectue des requetes à partir de l'ID
    """
    url = 'https://api.camptocamp.org/routes/' + str(document_id)
    r = util.open_url(url)
    return r

    
def parsage(data, type_request):
    """
        data : variable dictionnaire (json) renvoyée par la fonction 'client_search'
        type_request : waypoints OU routes

        Fonction qui parse le json renvoyé par l'API C2C en geojson
    """
    #result=open(outfile,'w') #Out file
    result_json=''
    wp, r =[], [] #liste vide permettant la concaténation des éléments au format convenable
    for i in range(len(data["documents"])): #Parcourt le fichier data
        geom = json.loads(data['documents'][i]['geometry']['geom']) #Récupère la géométrie
        lng = geom["coordinates"][0]
        lat = geom["coordinates"][1]
        id_point = data["documents"][i]["document_id"] #Récupère l'id
        
        #Selon ce qu'on cherche, la strucutre du json varie
        if type_request == 'waypoints':
            toponyme = data["documents"][i]["locales"][0]['title']
            elevation = data["documents"][i]["elevation"]
            #Concaténation de la liste au format GeoJson
            wp.append ({'type': 'Feature', 'id': id_point,'properties':{'id': id_point, 'nom': toponyme, 'coord': {'long' : lng, 'lat' : lat,}, 'altitude' : elevation, }, 'geometry' : geom })
        elif type_request=='routes':
            toponyme = data['documents'][i]["locales"][0]['title_prefix']
            elevation = data['documents'][i]["elevation_max"]
            #Concaténation de la liste au format GeoJson
            r.append ({'type': 'Feature', 'id': id_point,'properties':{'id': id_point, 'nom': toponyme, 'coord': {'long' : lng, 'lat' : lat,}, 'altitude' : elevation, }, 'geometry' : geom })
            trace_route = route(r[i]['id']) #Utilisation de la fonction 'route'
            r[i]['properties']['description']=trace_route['locales'][0]['description'] #Attribut "description" de la route
            geom2 = trace_route['geometry']['geom_detail'] #Géométrie de la polyligne correspondant au tracé GPS
            if geom2 != None:
                r[i]['geometry']=json.loads(geom2)
                # print(r[i]['geometry'])
    if type_request=='waypoints':
        result_json = wp
    elif type_request=='routes':
        result_json = r
    #resultat=json.dumps({'type': 'FeatureCollection', 'features':json.loads(result_json),}, indent=4, separators=(',', ': '))
    resultat={'type': 'FeatureCollection', 'features':result_json}
    return resultat


def iterate(url_temp, nb_result, a, bbox):
    """
        Effectue une boucle pour concaténer les différentes requetes (limite de 100 résultats par requete)
    """
    iteration = 100
    while (iteration < nb_result-100):
        url = url_temp + ';offset=' + str(iteration) + ';limit=100' + ';a=' + bbox
        b = util.open_url(url)
        iteration += 100
        a['documents'] += b['documents']
        # print('lala')
    url = url_temp + ';limit=' + str(nb_result-iteration) + ';offset=' + str(iteration) + ';a=' + bbox
    # print(url)
    b = util.open_url(url)
    a['documents'] += b['documents']
    return a