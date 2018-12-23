from PyQt5 import QtWidgets, QtGui, QtCore

class ObjectGraphics(QtWidgets.QGraphicsPixmapItem):
	def __init__(self, x,y,size,tile):
		self.tile = tile
		self.type = self.tile.get_graphics() #To be able to remember spawns after player are in them 

		name = self.type.lower()
		path = "graphics/{}.png".format(name)

		pixmap = QtGui.QPixmap(path)

		super().__init__(pixmap)

		icon_size = pixmap.width() #Assuming all icon are square
		
		factor = size/icon_size

		self.setScale(factor)

		originy = int(factor*pixmap.height()) - 52

		self.setPos(x,y-originy)
		
	def get_tile(self):
		return self.tile

	def get_type(self):
		return self.type
