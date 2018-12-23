from PyQt5 import QtWidgets, QtGui, QtCore

class TileGraphics(QtWidgets.QGraphicsPolygonItem):

	def __init__(self, x,y, width, height, tile):
		super().__init__()
		self.tile = tile
		self.width = width
		self.height = height


		self.setPolygon(self.construct_rhombus())

		self.setTransformOriginPoint(self.height, self.width)

		self.setPos(x,y)

		self.setPen(QtGui.QPen(QtGui.QColor(100,100,100))) # Set edges as grey

	#Higlight tile content with a color
	def update_color(self, highlight=(0,0,0)):
		
		if highlight[0] == highlight[1] == highlight[2] == 0:
			alpha = 0
		else:
			alpha = 80

		brush = QtGui.QBrush(QtGui.QColor(highlight[0], highlight[1], highlight[2], alpha))
		
		self.setBrush(brush)

	def construct_rhombus(self):

		iso_square = QtGui.QPolygonF()

		iso_square.append(QtCore.QPointF(self.width, 0))
		iso_square.append(QtCore.QPointF(2*self.width, self.height))
		iso_square.append(QtCore.QPointF(self.width,2*self.height))
		iso_square.append(QtCore.QPointF(0, self.height))
		iso_square.append(QtCore.QPointF(self.width, 0))

		return iso_square

	def get_tile(self):
		return self.tile