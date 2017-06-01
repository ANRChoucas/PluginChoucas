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
# Données issues de la base de données
#
#
# =============================================================================

from qgis.core import QgsVectorLayer
from qgis.core import QgsSvgMarkerSymbolLayerV2
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsDataSourceURI
from PyQt4.QtSql import *

import os

import util

# =============================================================================
#
#
# =============================================================================
def offline(root, source, type_pt):

    """
        Fonction qui va interroger une base de donnees et recuperer les donnees voulues
        Parametres:
            source: la source selectionnee
            type_pt: le type d entites a afficher
    """
    uri = QgsDataSourceURI()
    # On etablit la connection
    uri.setConnection("localhost", "5439", "choucas", "test", "test")


    # On recupere les attributs dans le catalogue
    table = util.get_second_object(root, source,type_pt,'table')
    geom = util.get_second_object(root, source,type_pt,'geom')
    # S il s agit d un point on recupere le style dans le catalogue
    if geom == 'Point':
        forme = util.get_second_object(root, source, type_pt, 'forme')
        couleur = util.get_first_object(root, source, 'couleur')
        svg = util.get_second_object(root, source,type_pt, 'svg')
        size_svg = util.get_second_object(root, source,type_pt, 'size')


    db = QSqlDatabase.addDatabase('QPSQL')
    # Verification de la validite de la connection
    if db.isValid():
        # Definition des parametres pour la connection
        db.setHostName(uri.host())
        db.setDatabaseName(uri.database())
        db.setPort(int(uri.port()))
        db.setUserName(uri.username())
        db.setPassword(uri.password())
        # Creation de la connection
        if db.open():
            # Requete a executer
            db.exec_("SELECT * from " + table) # 3 " a mettre autour de la requete

            # while query.next():
            #     # Pour afficher des donnees sur les resultats de la requete
            #     record = query.record()
            #     print record.field('id').value()

            # Pour afficher la table
            uri.setDataSource("it2", table, "geom",'')
            newLayer = QgsVectorLayer(uri.uri(), table, "postgres")

            # On attribut un style a la couche
            if geom == 'Point':
                if svg=='':
                    symbol = QgsMarkerSymbolV2.createSimple({'name': str(forme), 'color': str(couleur)})
                    newLayer.rendererV2().setSymbol(symbol)
                else:
                    svgStyle = {}
                    #svgStyle['fill'] = '#0000ff'
                    svgStyle['fill'] = '#00FFFF'
                    # Chemin ou se trouvent les styles
                    filename = os.path.join(os.path.dirname(__file__) + str('/styles/'),  str(svg) +'_'+ str(couleur) + '.svg')
                    svgStyle['name'] = filename
                    svgStyle['outline'] = '#000000'
                    svgStyle['outline-width'] = '6.8'
                    svgStyle['size'] = size_svg

                    symbol = QgsSvgMarkerSymbolLayerV2.create(svgStyle)
                    newLayer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol)

                if type_pt == 'lieux-dits habites' or type_pt == 'lieux-dits non habites':
                    newLayer.setCustomProperty("labeling", "pal")
                    newLayer.setCustomProperty("labeling/enabled", "true")
                    newLayer.setCustomProperty("labeling/fontFamily", "Arial")
                    newLayer.setCustomProperty("labeling/fontSize", "9")
                    newLayer.setCustomProperty("labeling/fieldName", "nom")
                    newLayer.setCustomProperty("labeling/placement", "2")

    
            QgsMapLayerRegistry.instance().addMapLayer(newLayer)
        
        else:
            print "QPSQL db not valid"
