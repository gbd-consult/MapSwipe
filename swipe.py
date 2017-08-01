from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
 
class SwipeMap(QgsMapCanvasMap):
    """A user defined QgsMapCanvasMap to draw an image and a rectangle
    
        Code is based on work from Nathan Woodrow
    """
    def __init__(self, canvas):
        super(SwipeMap, self).__init__(canvas)
        self.width = 0
        self.height = 0
        self.setZValue(-9.0)
        self.image = QImage()
        self.pen = QPen()
        self.pen.setColor(QColor("red"))
        self.opacity = 1.0
        
    def setContent(self, image, rect,  color=QColor("red"),  opacity = 1.0):
        """Set the content to draw
        
            :param image: The QImage to draw, usually generated from a render job
            :param rect: The rectangle to use to crop the image and to draw a crop rectangle
            :param color: The color (type QColor) of the rectangle to draw, default is white
            :param opacity: Set the opacity
        """
        self.image = image
        self.setRect(rect)
        self.pen.setColor(color)
        self.opacity = opacity
        
    def setWidth(self, width):
        self.width = width
        self.update()
        
    def setHeight(self, height):
        self.height = height
        self.update()
        
    def paint(self, painter, *args):
        w = self.width
        h = self.height
        image = self.image.copy(0, 0, w, h)
        painter.setOpacity(self.opacity)
        painter.drawImage(QRect(0, 0,w,h), image )
        painter.setPen(self.pen)
        painter.drawRect(0, 0,w,h)
