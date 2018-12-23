from PyQt5 import QtWidgets, QtGui, QtCore

class HitSplat(QtWidgets.QGraphicsItemGroup):

	def __init__(self, size, value):
		super().__init__()

		self.background = QtWidgets.QGraphicsEllipseItem(0,0,size,size)
		if value == 0:
			brush = QtGui.QBrush(QtGui.QColor(0,0,255))
		else:
			brush = QtGui.QBrush(QtGui.QColor(255,0,0))
		self.background.setBrush(brush) 
		self.addToGroup(self.background)

		#Hitsplat displays damage value
		self.text_item = QtWidgets.QGraphicsTextItem(str(value))

		#Hitsplat clolor based on damage
		if value < 10:
			self.text_item.setPos(6,0)
		else:
			self.text_item.setPos(2,0)


		self.text_item.setDefaultTextColor(QtGui.QColor(255,255,255))
		font = QtGui.QFont()
		font.setPixelSize(16)
		font.setBold(True)
		self.text_item.setFont(font)
		self.addToGroup(self.text_item)
