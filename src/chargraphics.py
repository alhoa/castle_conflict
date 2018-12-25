from PyQt5 import QtWidgets, QtGui, QtCore

#Character icon in GUI, has link to character
class CharGraphics(QtWidgets.QGraphicsPixmapItem):
	def __init__(self, x,y,size, character):


		directions = ["SW", "NE", "NW", "SE"]
		self.pixmaps = dict()

		#Read all directions to a dictionary
		for direction in directions:
			path = "characters/{}/icon{}.png".format(character.get_name().lower(),direction)
			self.pixmaps[direction] = QtGui.QPixmap(path) #No need for exeptions, Qpixmap will be white if image isn't found

		#Looking right is the default direction
		super().__init__(self.pixmaps["SE"])

		#Scale pixmapitem size
		#Pixmap() defined in QGraphicsPixmapItem
		self.height = self.pixmap().height()
		#Assuming all icons are square? and the same size
		icon_size = self.pixmap().width() 
		
		#Scale all icons to the same size
		self.factor = size/icon_size

		self.setScale(self.factor)

		originy = int(self.factor*self.height) - 52

		self.setPos(x,y-originy)

		self.setZValue(10000) #Spawn on top of other icons

		#Link to character
		self.char = character
		self.coords = self.char.get_coordinates()
		
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

	# Turns the character to face the direction of the last movement
	def turn(self,x,y):
		face = "SE" #Default facing

		if abs(x)>abs(y):
			if x < 0:
				face = "SW"
			elif x > 0:
				face = "NE"
		else:		
			if y < 0:
				face= "NW"
			elif y > 0:
				face= "SE"

		self.setPixmap(self.pixmaps[face])

	def get_height(self):
		return int(self.factor*self.height)
