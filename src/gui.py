from PyQt5 import QtWidgets, QtCore, QtGui

from tilegraphics import TileGraphics
from chargraphics import CharGraphics
from turntile import TurnTile
from hitsplat import HitSplat
from algorithms import find_route, find_los, find_area
from objectgraphics import ObjectGraphics
import random

#This class handles all graphical elements of the game

class GUI(QtWidgets.QMainWindow):

	def __init__(self, game):
		super().__init__()
		
		self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
		self.layout = QtWidgets.QGridLayout() #Use grid layout
		self.centralWidget().setLayout(self.layout)

		self.game = game
		self.game.set_gui(self)

		self.state = None #For defining tile highlights, Default to move after spawning
		self.busy = False #Disable buttons when game is busy
		self.walk_counter = 0 #To walk correct amout of pixels without having to call external methods

		self.WINDOW_HEIGHT = 720		#Dimensions for graphical window
		self.WINDOW_WIDTH = 1320

		self.highlighted_tiles = [] #List of highlighted tiles
		self.buttons = [] #Save buttons in separate list to simplify updating them

		self.enemy_timer = QtCore.QTimer()	#Enemy actions happen one at a time to follow them easier
		self.enemy_timer.setSingleShot(True)
		self.enemy_timer.timeout.connect(self.enemy_action)
		self.ENEMY_DELAY = 500	#Interval between wnwmy actions

		self.MAX_ATTACKS = 6
		self.TILE_HEIGHT = 26
		self.TILE_WIDTH = 45

		self.moving = None
		self.hitsplat_visible = False
		self.ended = False #Turn true when game ends to enable quitting with esc
	
		#Timer and settings for displaying hitsplats
		self.HITSPLAT_SIZE = 30
		self.HITSPLAT_COUNTER = 60

		#Initialize graphical elements
		self.init_window()
		self.init_log()
		self.init_grid()
		self.init_turnlist()
		self.init_objects()

		#Start spawning characters
		self.update_log("Select starting points for characters")
		self.game.spawn_enemies()

		# Update tiles periodically
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.on_timeout)
		self.timer.start(16) # around 60fps

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

		self.show()

	#Coordinate transformation from 2d to isometric
	def get_coordinate_position(self, coordinates):

		width = self.game.get_width()
		height = self.game.get_height()

		xorigin = int((self.WINDOW_WIDTH - (height+width)*self.TILE_WIDTH)/2)
		yorigin = int((self.WINDOW_HEIGHT -(height+width)*self.TILE_HEIGHT)/2-self.TILE_HEIGHT) # Move up by extra tile hight ???

		xpos = xorigin + (coordinates[0]+coordinates[1])*self.TILE_WIDTH     # 30 pixel gap on the edge
		ypos = yorigin + (width-coordinates[0]+coordinates[1])*26 # Y-coordinates are reversed??

		return (xpos, ypos)

	#Setup of all graphical objects
	def init_objects(self):

		width = self.game.get_width()
		height = self.game.get_height()

		#Loop through all tiles
		for y in range(height):
			for x in range(width):
				coords = (x,y)
				tile = self.game.get_tile(coords)

				position = self.get_coordinate_position(coords)

				if tile.is_graphical():
					marker = ObjectGraphics(position[0],position[1],2*self.TILE_WIDTH, tile)
					self.scene.addItem(marker)

		self.update_layers() #To ensure everything looks nice while spawning

	#Remove all spawn icons before game starts
	def clean_spawns(self):
		for item in self.scene.items():
			if type(item) is ObjectGraphics:
				if item.get_type() in ["PLAYER_SPAWN", "ENEMY_SPAWN"]:
					self.scene.removeItem(item)

	#setup log printing box
	def init_log(self):
		self.log = QtWidgets.QTextEdit(self)
		self.log.setReadOnly(True)
		self.layout.addWidget(self.log, 1,0,1,1)

	#setup map with background
	def init_grid(self):
		path = "maps/{}.png".format(self.game.get_mapname())
		pixmap = QtGui.QPixmap(path) #If file is not found, map will be white
		map = QtWidgets.QGraphicsPixmapItem(pixmap)
		self.scene.addItem(map)

		width = self.game.get_width()
		height = self.game.get_height()

		for y in range(height):
			for x in range(width):
				coords = (x,y)
				tile = self.game.get_tile(coords)


				#Only add necessay grid tiles
				if not tile.blocks_movement():
					position = self.get_coordinate_position(coords)
					rectangle = TileGraphics(position[0],position[1],self.TILE_WIDTH-1, self.TILE_HEIGHT-1, tile)
					self.scene.addItem(rectangle)

	#Add character graphical objects to the map
	def add_char(self, char):
		width = self.game.get_width()
		height = self.game.get_height()

		coords = char.get_coordinates()

		position = self.get_coordinate_position(coords)

		icon = CharGraphics(position[0],position[1], self.TILE_WIDTH*2, char)
		self.scene.addItem(icon)

	#Remove characters when they die
	def remove_character(self,char):
		icon = self.get_character_graphics(char)
		self.scene.removeItem(icon)

	#List of players in order of turns
	def init_turnlist(self):
		chars = self.game.get_characters()
		tilesize = 50
		spacing = tilesize + 20
		shift = 0

		for char in chars:
			turntile = TurnTile(10+shift, self.WINDOW_HEIGHT-tilesize-10,tilesize,char, self)
			shift += spacing

			self.scene.addItem(turntile)

		#Add turn indicator
		self.turn_highlight = QtWidgets.QGraphicsEllipseItem(13,self.WINDOW_HEIGHT-tilesize-7,tilesize-30, tilesize-30)
		brush = QtGui.QBrush(QtGui.QColor(255,255,255))
		self.turn_highlight.setBrush(brush)
		self.scene.addItem(self.turn_highlight)

	#Initialize rest of the game after spawn locations are chosen
	def init_game(self):

		self.init_labels()
		self.init_buttons()
		self.update_stats()
		self.clean_spawns()

		self.update_log("All characters added")

		self.game.initialize() #Initialize game

	#setup character informaton boxes
	def init_labels(self):

		self.label_group = QtWidgets.QGridLayout()

		self.name_label = QtWidgets.QLabel("Current character:")
		self.label_group.addWidget(self.name_label, 0,0,1,1)

		self.nameval_label = QtWidgets.QLabel(" ")
		self.label_group.addWidget(self.nameval_label, 0,1,1,1)

		self.level_label = QtWidgets.QLabel("Level:")
		self.label_group.addWidget(self.level_label, 1,0,1,1)

		self.level_val_label = QtWidgets.QLabel(" ")
		self.label_group.addWidget(self.level_val_label, 1,1,1,1)

		self.hp_label = QtWidgets.QLabel("HP:")
		self.label_group.addWidget(self.hp_label, 2,0,1,1)

		self.hpval_label = QtWidgets.QLabel(" ")
		self.label_group.addWidget(self.hpval_label, 2,1,1,1)

		self.ap_label = QtWidgets.QLabel("AP:")
		self.label_group.addWidget(self.ap_label, 3,0,1,1)

		self.apval_label = QtWidgets.QLabel(" ")
		self.label_group.addWidget(self.apval_label, 3,1,1,1)

		self.mp_label = QtWidgets.QLabel("MP:")
		self.label_group.addWidget(self.mp_label, 4,0,1,1)

		self.mpval_label = QtWidgets.QLabel(" ")
		self.label_group.addWidget(self.mpval_label, 4,1,1,1)

		self.label_box = QtWidgets.QGroupBox()
		self.label_box.setLayout(self.label_group)
		self.layout.addWidget(self.label_box, 1,1,1,1)

	#Create attack button group
	def init_buttons(self):

		self.button_group = QtWidgets.QGridLayout()

		next_icon = QtGui.QIcon(QtGui.QPixmap("graphics/end_turn_icon.png"))
		next_turn_btn = QtWidgets.QPushButton(next_icon,"")
		next_turn_btn.setIconSize(QtCore.QSize(50,50))
		next_turn_btn.setToolTip("Next turn")
		next_turn_btn.clicked.connect(lambda: self.parse_trigger("End turn"))
		self.button_group.addWidget(next_turn_btn, 0,0,1,1)

		self.buttons.append(next_turn_btn)

		x = 1	#Button placement
		y = 0

		for i in range(self.MAX_ATTACKS):

			btn = QtWidgets.QPushButton(QtGui.QIcon(),"")
			btn.setIconSize(QtCore.QSize(50,50))
			self.buttons.append(btn)
			btn.clicked.connect(lambda state, x=i: self.parse_trigger("Attack", x))
			self.button_group.addWidget(btn, y,x,1,1)
		
			y += 1
			if y > 1:
				y = 0
				x += 1
		
		self.group_box = QtWidgets.QGroupBox()
		self.group_box.setLayout(self.button_group)
		self.layout.addWidget(self.group_box, 1,2,1,1)

	#Update stats at every significant event, not every frame
	def update_stats(self):
		self.highlight_current()
		self.update_turnlist()
		self.update_labels()
		self.update_buttons()

	#Choose location of turn indicator on turn list
	def highlight_character(self, char):

		chars = self.game.get_characters()
		index = chars.index(char)
		self.turn_highlight.setRect(13+index*70,self.WINDOW_HEIGHT-50-7, 20, 20)

	#Highlight currently active player
	def highlight_current(self):
		char = self.game.get_current_character()
		self.highlight_character(char)

	#Return list of turn indicator items
	def get_turnlist(self):
		items = []
		for item in self.scene.items():
			if type(item) is TurnTile:
				items.append(item)
		
		return items

	#Update information in the turn list
	def update_turnlist(self):
		items = self.get_turnlist()
		
		index = 0
		chars = self.game.get_characters()

		for turntile in items:
			turntile.update_stats()
			if turntile.get_character() not in chars:
				self.scene.removeItem(turntile)
				for i in range(index):
					items[i].moveBy(-70,0)

			index += 1

	def update_labels(self):
		char = self.game.get_current_character()

		self.hpval_label.setText(str(char.get_hp()))
		self.apval_label.setText(str(char.get_ap()))
		self.mpval_label.setText(str(char.get_mp()))
		self.nameval_label.setText(char.get_name())
		self.level_val_label.setText(str(char.get_level()))

	#Change buttons for every character
	def update_buttons(self):

		char = self.game.get_current_character()
		attacks = char.get_attacks()

		index = 0 

		for attack in attacks:
			index += 1 #First button can't be changed
			if attack:
				name = attack.get_name().lower().replace(" ", "_")
				path = "attacks/{}.png".format(name)
				icon = QtGui.QIcon(QtGui.QPixmap(path))
				self.buttons[index].setToolTip(str(attack))
			else:
				icon = QtGui.QIcon(QtGui.QPixmap("graphics/block.png"))
				self.buttons[index].setToolTip("You do not have this attack")
			self.buttons[index].setIcon(icon)

	#Add hitsplat with timer
	def add_hitsplat(self,coords, val):

		hitsplat = HitSplat(self.HITSPLAT_SIZE, val)

		position = self.get_coordinate_position(coords)

		xpos = position[0] + self.TILE_WIDTH - self.HITSPLAT_SIZE/2 + random.randint(-10,10)
		ypos = position[1] - self.TILE_HEIGHT + 10 + random.randint(-10,10)

		hitsplat.setPos(xpos, ypos)


		hitsplat.setZValue(2000) #Hitsplats on top of everything

		self.scene.addItem(hitsplat)
		self.hitsplat_visible = True

	#move hitsplats and remove them after counter has reached set value
	def update_hitsplats(self):
		#Check if any hitsplats were found
		found = False

		for item in self.scene.items():
			if type(item) is HitSplat:
				found = True
				item.update_counter()

				if item.get_counter() > self.HITSPLAT_COUNTER:
					self.scene.removeItem(item)
				else:
					item.moveBy(0,-2)

		self.hitsplat_visible = found

	#Check if the character is currently carrying out an action
	def check_busy(self):
		if self.busy:
			value = False
		else:
			value = True

		for button in self.buttons:
			if button.toolTip() == "You do not have this attack":
				button.setEnabled(False)
			else:
				button.setEnabled(value)

	#List all isometric tile objects
	def get_tilegraphs(self):
		items = []
		for item in self.scene.items():
			if type(item) is TileGraphics:
				items.append(item)
		return items

	#Find tiles to highlight
	def find_highlights(self):
		tilegraphs = self.get_tilegraphs()
		self.highlighted_tiles = []

		if self.state == "Move":
			for tilegraph in tilegraphs:
				if tilegraph.isUnderMouse():
					coords = tilegraph.get_tile().get_coordinates()
					startloc = self.game.get_current_character().get_coordinates()

					self.highlighted_tiles = find_route(self.game,startloc,coords)

		elif self.state == "Attack":

			self.highlighted_tiles = self.game.get_current_character().get_attackable_coordinates()

	def on_timeout(self):
		self.update_tiles() #Always have highlighting connected
		self.update_layers()
		self.check_busy()

		if self.moving:
			self.move(self.moving[0],self.moving[1], self.moving[2], 2)

		if self.hitsplat_visible:
			self.update_hitsplats()


	#Add highlights to relevant tiles
	def update_tiles(self):
		self.find_highlights()
		mp = self.game.get_current_character().get_mp()

		tilegraphs = self.get_tilegraphs()

		#Go through all tiles to apply highlights
		for tilegraph in tilegraphs:
			if tilegraph.get_tile().get_coordinates() in self.highlighted_tiles:
				if self.state == "Move":
					if len(self.highlighted_tiles)>mp:
						tilegraph.update_color((100,0,0))
					else:
						tilegraph.update_color((0,255,0))
				elif self.state == "Attack":
					if tilegraph.isUnderMouse():
						tilegraph.update_color((100,0,0))
					else:
						tilegraph.update_color((0,150,255))
			elif tilegraph.isUnderMouse():
				tilegraph.update_color((100,0,0))
			else:
				tilegraph.update_color()

	#Update graphical item layer order
	def update_layers(self):
		items = []
		for item in self.scene.items():
			if type(item) is ObjectGraphics or type(item) is CharGraphics:
				items.append(item)
	
		for item in items:
			position = item.y()+item.get_height()
			item.setZValue(1000+position) #Add 1000 to prevent characters goind under bacground

	#Function to print informtaion to the log box
	def update_log(self, msg):
		self.log.append(msg)
		self.log.ensureCursorVisible() #Scroll down to see cursor

	#Determine actions based on trigger events
	def parse_trigger(self,msg,index=-1):

		if type(msg).__name__=='str':
			message = str(msg)
		else:
			message = msg.text()

		if message == "End turn": #Parse contents of message
			self.state = "Move"
			self.game.next_turn() #End the turn
			self.turn_type() # Check whether turn is player or enemy

		#For debugging
		elif message == "Kill":
			player = self.game.get_current_character()
			self.game.kill_character(player)

		elif message == "Attack":
			self.state = message
			self.game.get_current_character().choose_target(index)

		else:
			self.update_log(message)

	#Check if the active player is an enemy
	def turn_type(self):
		char = self.game.get_current_character()
		if char.is_controllable(): #Enable buttons and movement on player turns
			self.busy = False
			self.state = "Move"
		else:
			self.busy = True             #Disable buttons on enemy turns
			self.state = None			#Disable moving enemies
			self.enemy_timer.start(100) #Shorter dealy before first action 

	#Make one enemy action and wait for animation to end
	def enemy_action(self):
		char = self.game.get_current_character()
		if char.is_controllable(): #In case enemy in last turn suicides
			return

		if not char.is_busy():
			self.parse_trigger("End turn")
		else:
			char.make_action()
			self.enemy_timer.start(self.ENEMY_DELAY)

	#Return the graphic item representing a character
	def get_character_graphics(self,char):
		for item in self.scene.items():
			if type(item) is CharGraphics:
				if item.get_character() == char:
					icon = item
					break

		return icon

	#Move the graphical icon of the character
	def move_character(self, char):
		self.busy = True

		icon = self.get_character_graphics(char)

		coords = char.get_path()
		current = icon.get_coordinates()

		if current == coords[-1]:
			if char.is_controllable(): #Do not return buttons for enemies
				self.busy = False						 
			char.set_animating(False) #Mark that animation has ended
		else:
			if current in coords:
				target_index = coords.index(current)+1
			else:
				target_index = 0

			target = coords[target_index]
			x = target[0]-current[0]
			y = target[1]-current[1]
			icon.turn(x,y) #Turns the character adequately
			
			self.moving = (x,y, icon)

	#Animation loop for moving the character
	def move(self, x,y, item, speed):

		if self.walk_counter == 0:
			item.moveBy(15*(x+y),9*(y-x))
			self.walk_counter += 1
		elif self.walk_counter == 1:
			item.moveBy(15*(x+y),9*(y-x))
			self.walk_counter += 1
		elif self.walk_counter == 2:
			item.moveBy(15*(x+y),8*(y-x))
			self.walk_counter += 1
		else:
			self.moving = False
			self.walk_counter = 0
			item.move_coordinates(x,y)
			self.move_character(item.get_character())

	#End the game
	def end_game(self, msg):
		
		if msg[4] == "W":
			self.update_log("Congratulations, you won!")
		if msg[4] == "L":
			self.update_log("You lost, better luck next time.")
		#	self.enemy_timer.start(100) #Start timer and immediately stop it to prevent crash in case of suicide
			self.enemy_timer.timeout.disconnect() #Stop infinite loops in case enemies win
		self.update_log("Press ESC to exit")
		self.ended = True

	#Check where the user clicked
	def mousePressEvent(self, *args, **kwargs):
		
		tilegraphs = self.get_tilegraphs()

		#Operation during initialisation
		if not self.game.get_initialized():
			
			for tilegraph in tilegraphs:
				if tilegraph.isUnderMouse() and tilegraph.get_tile().is_player_spawn():
					coords = tilegraph.get_tile().get_coordinates()
					self.game.add_next_player(coords)

			self.game.spawn_enemies()

		#Operation during game
		else:
			for tilegraph in tilegraphs:
				if tilegraph.isUnderMouse():
					if self.state == "Attack":
						self.game.get_current_character().attack(tilegraph.get_tile().get_coordinates())
						self.state = "Move"
					elif self.state == "Move":
						char = self.game.get_current_character()
						coords = tilegraph.get_tile().get_coordinates()
						char.move(coords)

					else:
						tilegraph.update_color((0,100,0))
						self.update_log("Pressed tile:" + str(tilegraph.get_tile().get_coordinates()))

			turnlist = self.get_turnlist()

			for turntile in turnlist:
				pass

	def keyPressEvent(self,e):


		if e.key() == QtCore.Qt.Key_Escape:
			if self.ended:
				self.close() 	#Close window if game has ended
			else:
				self.state = "Move" #Stop actions with escape key

		if e.key() == QtCore.Qt.Key_G:
			self.close()

		#Hotkeys only work when buttons work and game is initialised
		if (not self.busy) and self.game.get_initialized():
			if e.key() == QtCore.Qt.Key_Space:
				self.parse_trigger("End turn")

			if e.key() == QtCore.Qt.Key_1:
				self.parse_trigger("Attack", 0)
			if e.key() == QtCore.Qt.Key_2:
				self.parse_trigger("Attack", 1)
			if e.key() == QtCore.Qt.Key_3:
				self.parse_trigger("Attack", 2)
			if e.key() == QtCore.Qt.Key_4:
				self.parse_trigger("Attack", 3)
			if e.key() == QtCore.Qt.Key_5:
				self.parse_trigger("Attack", 4)
			if e.key() == QtCore.Qt.Key_6:
				self.parse_trigger("Attack", 5)

