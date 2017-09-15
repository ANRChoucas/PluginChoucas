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
#   Fonctions utiles :
#  - gestion des listes déroulantes
#  - connection aux apis
#  - ...
# =============================================================================


import urllib2
import json


def get_first_object(root, source, objet):
        """
        Cette fonction permet de recuperer dans le catalogue un element situe juste apres la source (enfant de 1er degre)
        source: source selectionnee
        objet: objet recherche dans le catalogue
        """
        for child in root:
            name = child.get('name')
            if str(name) == str(source):
                result = child.find(str(objet)).text

        return result


def get_second_object(root, source, data, objet):
    """
        Cette fonction permet de recuperer dans le catalogue 
        un element situe juste apres l entite (enfant de 2nd degre par rapport a la source)
        source: source selectionnee
        type_pt: type d entite selectionne
        objet: objet recherche dans le catalogue
    """
    for child in root:
        name = child.get('name')
        if str(name) == str(source):
            for dat in child.iter('type'):
                if dat.get('data-id') == str(data):
                    result = dat.find(str(objet)).text
    return result
    

def get_attributs(root, nomSourceSelect, entite):
    """
        Retourne les attributs d'un type de données décrit dans le catalogue
    """
    attributs = {}
    for source in root:
        name = source.get('name')
        if str(name) == str(nomSourceSelect):
            for layer in source.iter('type'):
                if layer.get('data-id') == str(entite):
                    # result = dat.find(str(objet)).text
                    for attribut in layer.iter('attribut'):
                        attributs[attribut.get('name')] = {}
                        attributs[attribut.get('name')]['type'] = attribut.get('type')
                        attributs[attribut.get('name')]['chemin'] = attribut.text 
    return attributs
    
def getFiltres(root, nomSourceSelect, entite):
    """
        Retourne les filtres d'un type de données décrit dans le catalogue
    """
    filtres = {}
    for source in root:
        name = source.get('name')
        if str(name) == str(nomSourceSelect):
            for layer in source.iter('type'):
                if layer.get('data-id') == str(entite):
                    # result = dat.find(str(objet)).text
                    for filtre in layer.iter('filtre'):
                        filtres[filtre.get('cle') + '#' + filtre.get('valeur')] = filtre.get('type')
    return filtres
    


def chargeProxy(b):
    """
        Cette fonction permet de definir le proxy (cas particulier du proxy de l IGN)
        b: bouton (checkbox) selectionne en cas de particularite du proxy
    """
    if b.isChecked() == True:
        proxy = urllib2.ProxyHandler({
                'http': 'proxy.ign.fr:3128',
                'https': 'proxy.ign.fr:3128'
        })
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
    else:
        proxy = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        

def open_url(url):
    """
        Fonction qui utilise la librairie urllib2 (Python 2.7) pour faire des requete HTTP
        url : url a interroger pour la requete
    """
    # print(url)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    data = json.load(response)
    return data
