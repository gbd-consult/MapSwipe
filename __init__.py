# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapSwipe
                                 A QGIS plugin
 Map swipe tool
                             -------------------
        begin                : 2015-01-09
        copyright            : (C) 2015 by Geoinformatikbüro Dassau GmbH
        email                : dassau@gbd-consult.de
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
    """Load MapSwipe class from file MapSwipe.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .mapswipe import MapSwipe
    return MapSwipe(iface)
