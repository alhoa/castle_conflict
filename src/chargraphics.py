from PyQt5 import QtWidgets, QtGui, QtCore

#Character icon in GUI, has link to character
class CharGraphics(QtWidgets.QGraphicsPixmapItem):
	def __init__(self, x,y,size, character):


		path = "characters/{}/icon.png".format(character.get_name().lower())
		pixmap = QtGui.QPixmap(path) #No need for exeptions, Qpixmap will be white if image isn't found
		super().__init__(pixmap)
		self.char = character
		self.coords = self.char.get_coordinates()

		#Assuming all icon are square
		icon_size = pixmap.width() 
		
		#Scale all icons to the same size
		factor = size/icon_size

		self.setScale(factor)

		originy = int(factor*pixmap.height()) - 52

		self.setPos(x,y-originy)

		self.setZValue(10000) #Spawn on top of icons

		
	#Check if icon is at the correct position
	def at_character_position(self):
		if self.coords == self.character.get_coordinates():
			return True
		else:
			return False

	def move_coordinates(self, x,y):
		self.coords = (self.coords[0]+x, self.coords[1]+y)

	def get_coordinates(self):
		return self.coords

	def get_character(self):
		return self.char
