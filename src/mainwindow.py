from PyQt5 import QtWidgets, QtCore, QtGui
from gui import GUI
from resultwindow import ResultWindow
from saveparser import SaveParser
from chargraphics import CharGraphics
from exceptions import *

import random

#This class handles all graphical elements of the game

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self):
		super().__init__()
		
		self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
		self.layout = QtWidgets.QGridLayout() #Use grid layout
		self.centralWidget().setLayout(self.layout)

		self.WINDOW_HEIGHT = 650		#Dimensions for graphical window
		self.WINDOW_WIDTH = 720
		self.ICON_SIZE = 175 #Window can fit 4 icons

		self.buttons = [] #Save buttons in separate list to simplify updating them

		#Initialize graphical elements
		self.init_window()
		self.init_log()
		self.init_buttons()

		self.show()

		self.parser = None
		self.game_gui = None
		self.active_game = None
		self.players = []

		self.game_index = 0
		self.num_games = 0

		self.update_log("Welcome!")
		self.update_log("Press load save to start a game")


	#Setup of the graphical window
	def init_window(self):

		self.setGeometry(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT) #Leave room for log box
		self.setWindowTitle('Strategy game V1.0')

		# Add a scene for drawing 2d objects
		self.scene = QtWidgets.QGraphicsScene()
		self.scene.setSceneRect(0, 0, self.WINDOW_WIDTH-20,self.WINDOW_HEIGHT-240)

		# Add a view for showing the scene
		self.view = QtWidgets.QGraphicsView(self.scene, self)
		self.layout.addWidget(self.view, 0,0,1,2)

		pixmap = QtGui.QPixmap("graphics/title.png")
		self.splash_screen = QtWidgets.QGraphicsPixmapItem(pixmap)
		self.splash_screen.setScale(0.4)
		self.scene.addItem(self.splash_screen)

	def update_window(self):
		#Cleanup window
		self.scene.clear()

		self.scene.setSceneRect(0, 0, self.WINDOW_WIDTH-20,self.WINDOW_HEIGHT-450)
		shift = 0

		for player in self.players:
			icon = CharGraphics(shift, 0, self.ICON_SIZE, player)
			icon.moveBy(0,icon.get_height()-50)
			self.scene.addItem(icon)
			shift += self.ICON_SIZE

		self.add_char_information()

	def add_char_information(self):

		shift = 0
		self.info_group = QtWidgets.QGridLayout()


		column_width = 90

		for i in range(8):
			self.info_group.setColumnMinimumWidth(i, column_width)

		for player in self.players:

			name_label = QtWidgets.QLabel(player.get_name())
			self.info_group.addWidget(name_label, 0,shift,1,1)

			level_label = QtWidgets.QLabel(str(player.get_level()))
			self.info_group.addWidget(level_label, 0,shift+1,1,1)

			hp_label = QtWidgets.QLabel("HP:")
			self.info_group.addWidget(hp_label, 1,shift,1,1)

			hpval_label = QtWidgets.QLabel(str(player.get_hp()))
			self.info_group.addWidget(hpval_label, 1,shift+1,1,1)

			ap_label = QtWidgets.QLabel("AP:")
			self.info_group.addWidget(ap_label, 2,shift,1,1)

			apval_label = QtWidgets.QLabel(str(player.get_ap()))
			self.info_group.addWidget(apval_label, 2,shift+1,1,1)

			mp_label = QtWidgets.QLabel("MP:")
			self.info_group.addWidget(mp_label, 3,shift,1,1)

			apval_label = QtWidgets.QLabel(str(player.get_mp()))
			self.info_group.addWidget(apval_label, 3,shift+1,1,1)

			inv_btn = QtWidgets.QPushButton("Inventory")
			inv_btn.setToolTip("Open inventory")
			self.info_group.addWidget(inv_btn, 4,shift,1,2)

			stat_btn = QtWidgets.QPushButton("Stats")
			stat_btn.setToolTip("Open stats")
			self.info_group.addWidget(stat_btn, 5,shift,1,2)

			shift += 2

		


		group_box = QtWidgets.QGroupBox()
		group_box.setLayout(self.info_group)
		self.layout.addWidget(group_box, 1, 0, 1, 2)


	#setup log printing box
	def init_log(self):
		self.log = QtWidgets.QTextEdit(self)
		self.log.setReadOnly(True)
		self.layout.addWidget(self.log, 2,0,1,1)

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
		self.layout.addWidget(self.group_box, 2,1,1,1)

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

		except CorruptedSaveError as msg:
			self.update_log(msg)

		#Check how many games were read
		self.num_games = self.parser.get_num_games()
		self.update_log("Loaded {} games".format(self.num_games))

		self.players = self.parser.get_loaded_players()
		self.update_window()

	def start_game(self):
		if self.game_index < self.num_games:
			self.active_game = self.parser.get_game(self.game_index)
			#Clumsy way to move forward
			self.game_index += 1

			#Start game
			self.game_gui = GUI(self.active_game)
			self.game_gui.end_signal.connect(self.end_game)


		elif self.parser == None:
			self.update_log("No save loaded")
		else:
			self.update_log("Not enough games loaded")

	def end_game(self):

		self.update_log("Game ended")

		self.ResultWindow = ResultWindow(self.active_game)

		for player in self.players:
			player.store_xp()
			player.set_xp(0)
			player.set_coordinates(None)
			player.set_hp(player.get_hp_max())
			player.set_ap(player.get_ap_max())
			player.set_mp(player.get_mp_max())

		self.active_game = None

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