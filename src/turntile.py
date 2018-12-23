from PyQt5 import QtWidgets, QtGui, QtCore
from tile import Tile

#Contains character icon and amount of health

class TurnTile(QtWidgets.QGraphicsItemGroup):

	def __init__(self, x,y, square_size, character, gui):
		super().__init__()
		self.character = character
		self.gui = gui # To be able to use log printing

		#Backgound color basen on faction
		self.rectangle_background = QtWidgets.QGraphicsRectItem(x-3,y-3,square_size+6,square_size+6)
		if self.character.is_controllable():
			brush = QtGui.QBrush(QtGui.QColor(25,50,200)) # Blue = player
		else:
			brush = QtGui.QBrush(QtGui.QColor(200,25,25)) # Red = enemy
		self.rectangle_background.setBrush(brush) 
		self.addToGroup(self.rectangle_background)

		#Get character icon
		path = "characters/{}/icon.png".format(character.get_name().lower())
		pixmap = QtGui.QPixmap(path)
		self.char_icon = QtWidgets.QGraphicsPixmapItem(pixmap)
		self.char_icon.setPos(x,y)

		icon_size = pixmap.width() #Assuming all icon are square
		factor = square_size/icon_size
		self.char_icon.setScale(factor)
		self.addToGroup(self.char_icon)

		#Add hp text
		self.text_item = QtWidgets.QGraphicsTextItem()
		self.update_stats()
		self.text_item.setPos(x,y+square_size-24)
		self.text_item.setDefaultTextColor(QtGui.QColor(255,255,255))
		font = QtGui.QFont()
		font.setPixelSize(16)
		font.setBold(True)
		self.text_item.setFont(font)
		self.addToGroup(self.text_item)

	def get_character(self):
		return self.character

	def update_stats(self):
		text = "{hp}/{max_hp}".format(hp=self.character.get_hp(), max_hp = self.character.get_hp_max())
		self.text_item.setPlainText(text)

	#Print player information when clicked on
	def mousePressEvent(self, *args, **kwargs):
		if self.isUnderMouse():
			self.gui.update_log(str(self.character))