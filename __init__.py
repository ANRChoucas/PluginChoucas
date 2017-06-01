# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PluginChoucas
                                 A QGIS plugin
 Ce plugin permet la visualisation de données de montagne provenant de différentes API 
                             -------------------
        begin                : 2017-03-15
        copyright            : (C) 2017 by Coline Eva Sylvain
        email                : eva.chenyensu@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PluginChoucas class from file PluginChoucas.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .plugin_choucas import PluginChoucas
    return PluginChoucas(iface)
