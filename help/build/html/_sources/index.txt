Welcome to MapSwipe's documentation!
============================================

The MapSwipe plugin is designed to compare two raster or vector layers using
an overlay mechanism called swiping. At the moment a single layer can be used as overlay, 
while any amount of layers (raster and vector) can be used in the background.
Zooming, panning and object querying is fully supported in swipe mode.

.. toctree::
   :maxdepth: 2
   :numbered:

Getting started
---------------

To compare two images using the MapSwipe plugin we must first load two layers 
into QGIS. In this example we compare two satellite images from Japan that shows
the situation before and after the Tsunami catastrophe from 2011 that 
are available here [NASA]_.

.. figure:: Snapshot_1.png
	:scale: 50%
	:align: center

	QGIS with two satellite images from Japan to investigate 
	the Tsunami aftermath from 2011.
	
The MapSwipe plugin can be started from the extension menu 
:menuselection:`Extensions --> MapSwipe` or
using the MapSwipe symbol |icon| in the toolbar of QGIS. The manual page is
available in the :menuselection:`Extensions --> MapSwipe` menu.


.. |icon| image:: icon.png
    :width: 2 em

When started, three new GUI components will appear within the QGIS window. 
The main widget on the left side with which the the swipe mechanism 
can be started and stopped. In addition
the color of the overlay rectangle and the opacity of the overlay
can be specified. Two slider widgets
are placed below the map window and on the right side. These slider will modify 
size of the overlay rectangle in horizontal and vertical directions. 
They can be placed outside of QGIS as well.

.. figure:: Snapshot_2.png
	:scale: 50%
	:align: center

	Activated MapSwipe plugin showing the main GUI component and the two sliders.
	
To enable the swipe mechanism the *Start* button must be pressed. **The current selected
layer will be used to create the map overlay.** Its name will appear
in the *Selected layer* section of the MapSwipe main widget. 
The selected layer will be disabled
in the layer window and the overlay window will be created. The *Stop* button
will remove the overlay and disable the slider, color and opacity chooser.

.. figure:: Snapshot_3.png
	:scale: 50%
	:align: center

	Swipe sliders in vertical position. The left half shows the region of 
	Japan before the Tsunami, the right half shows the region after the Tsunami 
	impact.


.. [NASA] http://earthobservatory.nasa.gov/NaturalHazards/view.php?id=49634

Overlay size and layout
-----------------------

The sliders can be used to create an overlay rectangle of arbitrary size. The
sliders can be setup to allow vertical and horizontal mode.

.. figure:: Snapshot_5.png
	:scale: 50%
	:align: center

	Setting the sliders up to an arbitrary sized rectangle.
	

.. figure:: Snapshot_6.png
	:scale: 50%
	:align: center

	Setting the sliders to enable horizontal swiping.

Rectangle color and opacity
---------------------------

The opacity of the overlay can be modified in the MapSwipe main GUI component.
The opacity can be set from fully transparent (0) to full opaque (100). In addition
the color of the rectangle can be set to different colors.

.. figure:: Snapshot_7.png
	:scale: 50%
	:align: center

	Modification of the rectangle color to white and overlay opacity to 60.
	
The color, opacity settings and the slider 
positions are temporary stored, so that the MapSwipe tool can be enabled and disabled
without loosing the current settings. The settings will be lost, when QGIS gets restarted.
