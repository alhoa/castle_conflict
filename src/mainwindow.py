from PyQt5 import QtWidgets, QtCore, QtGui
from gui import GUI
from saveparser import SaveParser
from exceptions import *

import random

#This class handles all graphical elements of the game

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self):
		super().__init__()
		
		self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
		self.layout = QtWidgets.QGridLayout() #Use grid layout
		self.centralWidget().setLayout(self.layout)

		self.WINDOW_HEIGHT = 410		#Dimensions for graphical window
		self.WINDOW_WIDTH = 700

		self.buttons = [] #Save buttons in separate list to simplify updating them

		#Initialize graphical elements
		self.init_window()
		self.init_log()
		self.init_buttons()

		self.parser = None

		self.game_index = 0
		self.num_games = 0

		self.update_log("Welcome!")
		self.update_log("Press load save to start a game")


	#Setup of the graphical window
	def init_window(self):

		self.setGeometry(0, 0, self.WINDOW_WIDTH+20, self.WINDOW_HEIGHT+260) #Leave room for log box
		self.setWindowTitle('Strategy game V1.0')

		# Add a scene for drawing 2d objects
		self.scene = QtWidgets.QGraphicsScene()
		self.scene.setSceneRect(0, 0, self.WINDOW_WIDTH,self.WINDOW_HEIGHT)

		# Add a view for showing the scene
		self.view = QtWidgets.QGraphicsView(self.scene, self)
		self.layout.addWidget(self.view, 0,0,1,4)

		pixmap = QtGui.QPixmap("graphics/title.png")
		pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
		pixmap_item.setScale(0.4)
		self.scene.addItem(pixmap_item)

		self.show()

	#setup log printing box
	def init_log(self):
		self.log = QtWidgets.QTextEdit(self)
		self.log.setReadOnly(True)
		self.layout.addWidget(self.log, 1,0,1,1)

	def init_buttons(self):

		self.button_group = QtWidgets.QGridLayout()

		load_icon = QtGui.QIcon(QtGui.QPixmap("graphics/open.png"))
		load_btn = QtWidgets.QPushButton(load_icon,"")
		load_btn.setIconSize(QtCore.QSize(50,50))
		load_btn.setToolTip("Load save")
		load_btn.clicked.connect(lambda: self.parse_trigger("Load game"))
		self.button_group.addWidget(load_btn, 0,0,1,1)
		self.buttons.append(load_btn)

		start_icon = QtGui.QIcon(QtGui.QPixmap("graphics/arrow.png"))
		start_btn = QtWidgets.QPushButton(start_icon,"")
		start_btn.setIconSize(QtCore.QSize(50,50))
		start_btn.setToolTip("Start game")
		start_btn.clicked.connect(lambda: self.parse_trigger("Start game"))
		self.button_group.addWidget(start_btn, 1,0,1,1)
		self.buttons.append(start_btn)

		self.group_box = QtWidgets.QGroupBox()
		self.group_box.setLayout(self.button_group)
		self.layout.addWidget(self.group_box, 1,2,1,1)

	def load_game(self):

		#Reset game counter
		self.game_index = 0

		#Create new parser 
		try:
			self.parser = SaveParser()
		except CorruptedSaveError as msg:
			self.update_log(msg)

		#inform player about loaded enemies
		self.update_log("Loaded enemies:")
		enemies = self.parser.get_loaded_enemies()
		for key in enemies:
			self.update_log("Name: {name},    Level: {level}".format(name=key[0], level = key[1]))

		#Show dialog window to choose save file
		dialog = QtWidgets.QFileDialog()
		dialog.setDirectory("saves/")
		fname = dialog.getOpenFileName(None, 'Castle Conflict - Choose save file')

		save_path = fname[0]

		try:
			self.parser.read_save(save_path)

			#Check how many games were read
			self.num_games = self.parser.get_num_games()
			self.update_log("Loaded {} games".format(self.num_games))
		except CorruptedSaveError as msg:
			self.update_log(msg)

	def start_game(self):
		if self.game_index < self.num_games:
			game = self.parser.get_game(self.game_index)
			#Clumsy way to move forward
			self.game_index += 1

			#Start game
			self.gui = GUI(game)
		elif self.parser == None:
			self.update_log("No save loaded")
		else:
			self.update_log("Not enough games loaded")


	def parse_trigger(self,msg,index=-1):

		if type(msg).__name__=='str':
			message = str(msg)
		else:
			message = msg.text()

		if message == "Load game": #Parse contents of message
			self.load_game()
			
		elif message == "Start game":
			self.start_game()

		else:
			self.update_log(message)

	def update_log(self, msg):
		self.log.append(msg)
		self.log.ensureCursorVisible() #Scroll down to see cursor