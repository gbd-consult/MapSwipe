# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapSwipe
                                 A QGIS plugin
 Map swipe tool
                              -------------------
        begin                : 2015-01-09
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Geoinformatikbüro Dassau GmbH
        email                : dassau@gbd-consult.de
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
from PyQt4.QtCore import *
from PyQt4.QtGui import QAction, QIcon, QSlider, QColor,  QColorDialog,  QPalette
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from mapswipe_bottom_dock import MapSwipeBottomDockWidget
from mapswipe_right_dock import MapSwipeRightDockWidget
from mapswipe_dockwidget import MapSwipeDockWidget
from swipe import SwipeMap
import os.path
from qgis.gui import *
from qgis.core import *
from qgis import utils

# 4K Display
swipeSliderMaximum = 4000

class MapSwipe:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.rightDock = MapSwipeRightDockWidget()
        self.bottomDock = MapSwipeBottomDockWidget()
        self.selectDock = MapSwipeDockWidget()
        
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&MapSwipe')
        self.toolbar = self.iface.addToolBar(u'MapSwipe')
        self.toolbar.setObjectName(u'MapSwipe')
        
        self.selectDock.startButton.clicked.connect(self.startButtonClicked)
        self.selectDock.stopButton.clicked.connect(self.stopButtonClicked)
        self.selectDock.colorChooserButton.clicked.connect(self.colorChoseButtonClicked)
        self.selectDock.spinBoxOpacity.valueChanged.connect(self.opacityValueChanged)
        QgsMapLayerRegistry.instance().layersRemoved.connect(self.checkActiveLayerRemoved)

        self.overlayMap = SwipeMap(self.iface.mapCanvas())
        self.overlayMap.hide()
        self.layerId = None
        self.rectColor = QColor("red")
        self.overlayOpacity = 1.0
        self.firstRun = True
        self.colorDialog = QColorDialog(self.rectColor,  parent=self.iface.mainWindow())
        self.selectDock.colorChooserButton.setPalette(QPalette(self.rectColor))
        
        # Setup the slider resolution and values
        self.bottomDock.Slider.setMaximum(swipeSliderMaximum)
        self.bottomDock.Slider.setTickInterval(swipeSliderMaximum/100)
        self.rightDock.Slider.setMaximum(swipeSliderMaximum)
        self.rightDock.Slider.setTickInterval(swipeSliderMaximum/100)
        self.rightDock.Slider.setValue(swipeSliderMaximum)
        self.bottomDock.Slider.setValue(swipeSliderMaximum/2)

        self.init_default_settings()

    def init_default_settings(self):
        settings = QSettings()
        if not settings.value( "/MapSwipe/rightSlideValue" ) is None:
            settings.setValue("/MapSwipe/rightSlideValue",  swipeSliderMaximum)
        if not settings.value( "/MapSwipe/bottomSlideValue" ) is None:
            settings.setValue("/MapSwipe/bottomSlideValue",  swipeSliderMaximum/2)
        if not settings.value( "/MapSwipe/selectDockColorIndex" ) is None:
            settings.setValue("/MapSwipe/selectDockColorIndex" , 0)
        if not settings.value( "/MapSwipe/selectDockOpacityValue" ) is None:
            settings.setValue("/MapSwipe/selectDockOpacityValue" ,  100)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MapSwipe', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = ':/plugins/MapSwipe/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'MapSwipe'),
            callback=self.run,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/MapSwipe/help_icon.png'
        self.add_action(
            icon_path=icon_path, 
            text = self.tr(u'Manual'),
            callback = self.open_help_in_browser,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=False,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&MapSwipe'),
                action)
            self.iface.removeToolBarIcon(action)

        self.clearSwipeLayer()
        
        if self.firstRun == False:
            self.iface.removeDockWidget(self.rightDock)
            self.iface.removeDockWidget(self.bottomDock)
            self.iface.removeDockWidget(self.selectDock)
 
    def run(self):
        # show the dockable widgets
        if self.firstRun == True:
            self.iface.addDockWidget( Qt.BottomDockWidgetArea, self.bottomDock)
            self.iface.addDockWidget( Qt.RightDockWidgetArea, self.rightDock)    
            self.iface.addDockWidget( Qt.LeftDockWidgetArea, self.selectDock)       
            self.bottomDock.show()
            self.rightDock.show()
            self.selectDock.show()
            self.disableButtons()
        elif self.bottomDock.isVisible() and self.rightDock.isVisible() \
           and self.selectDock.isVisible():

            self.bottomDock.hide()
            self.rightDock.hide()
            self.selectDock.hide()
            self.overlayMap.hide()
            self.clearSwipeLayer()
        else:
            self.bottomDock.show()
            self.rightDock.show()
            self.selectDock.show()
        
        self.firstRun = False
        
    def enableButtons(self):
        self.rightDock.Slider.setEnabled(True)
        self.bottomDock.Slider.setEnabled(True)
        self.selectDock.spinBoxOpacity.setEnabled(True)
        self.selectDock.colorChooserButton.setEnabled(True)
        
    def disableButtons(self):
        self.rightDock.Slider.setEnabled(False)
        self.bottomDock.Slider.setEnabled(False)
        self.selectDock.spinBoxOpacity.setEnabled(False)
        self.selectDock.colorChooserButton.setEnabled(False)

    def startButtonClicked(self):
        self.setupSwipeLayer()
        self.enableButtons()
        
    def stopButtonClicked(self):
        self.clearSwipeLayer()
        
    def opacityValueChanged(self):
        self.overlayOpacity = self.selectDock.spinBoxOpacity.value()/100.0
        self.iface.mapCanvas().refresh()

    def colorChoseButtonClicked(self):
        self.colorDialog.show()
        result = self.colorDialog.exec_()
        if result:
            self.selectDock.colorChooserButton.setPalette(QPalette(self.colorDialog.currentColor()))
            self.rectColor = self.colorDialog.currentColor()
            self.iface.mapCanvas().refresh()

    def setupSwipeLayer(self):
        """Setup the swipe functionality"""
        # Clear all before generate new
        self.clearSwipeLayer()
        if self.iface.activeLayer() is not None:
            self.iface.legendInterface().setLayerVisible(self.iface.activeLayer(),  False)
            self.layerId = self.iface.activeLayer().id()
            self.selectDock.layerNameLabel.setText("<b>" + self.iface.activeLayer().name() + "</b>")

            # Connect the slider
            self.bottomDock.Slider.valueChanged.connect(self.width_value)
            self.rightDock.Slider.valueChanged.connect(self.height_value)

            # Create the render job
            self.iface.mapCanvas().mapCanvasRefreshed.connect(self.updateBackMap)            
            self.overlayMap.show()

            settings = QSettings()
            self.bottomDock.Slider.setValue(int(settings.value( "/MapSwipe/bottomSlideValue" )))
            self.rightDock.Slider.setValue(int(settings.value( "/MapSwipe/rightSlideValue" )))
            
            self.colorDialog.setCurrentColor(settings.value( "/MapSwipe/selectDockColor" ))
            self.rectColor = self.colorDialog.currentColor()
            
            self.selectDock.spinBoxOpacity.setValue(int(settings.value( "/MapSwipe/selectDockOpacityValue" )))
            self.overlayOpacity = self.selectDock.spinBoxOpacity.value()/100.0

            self.width_value(self.bottomDock.Slider.value())
            self.height_value(self.rightDock.Slider.value())
            self.iface.mapCanvas().refresh()

    def clearSwipeLayer(self):
        """Disconnect several callback functions and store the settings"""
        try:
            self.bottomDock.Slider.valueChanged.disconnect(self.width_value)
            self.rightDock.Slider.valueChanged.disconnect(self.height_value)
            self.iface.mapCanvas().mapCanvasRefreshed.disconnect(self.updateBackMap)
        except TypeError:
            pass

        settings = QSettings()
        settings.setValue( "/MapSwipe/bottomSlideValue",  self.bottomDock.Slider.value( ))
        settings.setValue( "/MapSwipe/rightSlideValue",  self.rightDock.Slider.value())
        settings.setValue( "/MapSwipe/selectDockColor", self.colorDialog.currentColor())
        settings.setValue( "/MapSwipe/selectDockOpacityValue",  self.selectDock.spinBoxOpacity.value())

        # Hide the overlay and disable the silder
        self.overlayMap.hide()
        self.disableButtons()
        self.selectDock.layerNameLabel.setText("...")

    def checkActiveLayerRemoved(self):
        """Check if the swipe layer was removed from the layer register"""
        if  QgsMapLayerRegistry is not None and QgsMapLayerRegistry.instance() is not None:
            layer = QgsMapLayerRegistry.instance().mapLayer(self.layerId)

            # If the layer was removed, stop the swipe tool
            if layer is None:
                self.clearSwipeLayer()

    def width_value(self,  i):
        """Callback function used by the horizontal slider to update the 
            drawable overlay image rectangle"""
        w = (i * self.iface.mapCanvas().map().boundingRect().width()) / float(swipeSliderMaximum)
        self.overlayMap.setWidth(w)

    def height_value(self,  i):
        """Callback function used by the vertical slider to update the 
            drawable overlay image rectangle"""
        h = (i * self.iface.mapCanvas().map().boundingRect().height()) / float(swipeSliderMaximum)
        self.overlayMap.setHeight(h)

    def updateBackMap(self):
        """Callback that is called at the refresh event of the map canvas"""
        def updatemap():
            """Callback to draw the overlay map layer and the rectangle"""
            self.overlayMap.setContent(job.renderedImage(), settings.visibleExtent(),  
                                                         self.rectColor, self.overlayOpacity)

        # We need to start a parallel render job to draw the overlay image
        settings = QgsMapSettings(self.iface.mapCanvas().mapSettings())
        settings.setLayers((self.layerId, ))
        job = QgsMapRendererParallelJob(settings)
        job.finished.connect(updatemap)
        job.start()
        job.waitForFinished ()

    def open_help_in_browser(self):
        import webbrowser, os
        webbrowser.open(os.path.join(self.plugin_dir,  "help",  "build", "html",  "index.html"))
