from tile import Tile
import random

#Handles core game mechanics such as turns and tile contents

class Game():

	def __init__ (self, width, height, characters, mapname):

		self.tiles = [None] * width

		for x in range(self.get_width()):
			self.tiles[x] = [None] * height
			for y in range(self.get_height()):
				self.tiles[x][y] = Tile((x,y))	# All tiles are initialized as empty

		self.characters = characters
		self.turn = 0
		self.initialized = False
		self.gui = None
		self.mapname = mapname

	def get_mapname(self):
		return self.mapname

	def set_gui(self, gui):
		self.gui = gui

	def get_gui(self):
		return self.gui

	def get_width(self):
		return len(self.tiles)

	def get_height(self):
		return len(self.tiles[0])

	def get_tile(self, coordinates):
		if self.in_bounds(coordinates):
			return self.tiles[coordinates[0]][coordinates[1]]
		else:
			return Tile((-1,-1),True)

	def get_tiles(self):
		return self.tiles

	def in_bounds(self, coordinates):
		return 0 <= coordinates[0] < self.get_width() and 0 <= coordinates[1] < self.get_height()

	def get_characters(self):
		return self.characters

	def get_players(self):
		players = []
		for char in self.characters:
			if char.is_controllable():
				players.append(char)

		return players

	def get_current_character(self):
		if len(self.characters) > 0:
			return self.characters[self.turn]
		else:
			return None

	def next_turn(self):
		char = self.get_current_character()
		char.end_turn()

		num_characters = len(self.characters)
		self.turn = (self.turn+1)%num_characters

		char = self.get_current_character()

		char.init_turn()
		self.gui.update_stats()

	def set_tile_contents(self,coordinates,blocks_vision, blocks_movement, graphics):
		self.get_tile(coordinates).set_blocks_vision(blocks_vision)
		self.get_tile(coordinates).set_blocks_movement(blocks_movement)
		self.get_tile(coordinates).set_graphics(graphics)

	#For adding both players and enemies to the game
	def add_character(self,coordinates, character):

		if self.get_tile(coordinates).set_character(character):
			character.set_coordinates(coordinates)
			character.set_game(self)
			self.get_tile(coordinates).set_graphics(None) ##Remove spawner
		
		self.gui.update_log("Selected position for "+ character.get_name())

	#Enemies added by random
	def add_enemy(self, enemy):
		spawn_tiles = []

		for line in self.tiles:
			for tile in line:
				if tile.is_enemy_spawn():
					spawn_tiles.append(tile)

		index = random.randint(0,len(spawn_tiles)-1)
		coords = spawn_tiles[index].get_coordinates() #Choose random spawn point

		self.add_character(coords, enemy)

	#Spawn all enemies before next active player
	def spawn_enemies(self):

		next_char = None

		for char in self.characters:

			#Find all unadded characters
			if char.get_coordinates() == None:
				if not char.is_controllable():
					self.add_enemy(char)
					self.gui.add_char(char)
				else:
					next_char = char #Next player to be spawned
					break

		if next_char == None:
			self.gui.init_game() #Finish up initializng if no players are left
			self.gui.parse_trigger("End turn") #Take first turn here 
		else:
			self.gui.highlight_character(next_char) #Highlight next character to be placed


	def add_next_player(self, coordinates):
		for char in self.get_players():
			if char.get_coordinates() == None:
				self.add_character(coordinates, char)
				self.gui.add_char(char)
				return


	def get_initialized(self):
		return self.initialized

	def initialize(self):
		#Remove all spawns
		self.initialized = True
		for line in self.tiles:
			for tile in line:
				if tile.is_enemy_spawn() or tile.is_player_spawn():
					tile.set_graphics(None)

		#Set turn to last so that next turn is on first player
		self.turn = len(self.characters)-1


	def kill_character(self, character):

		suicide = False

		#Check if character suicided
		if character == self.get_current_character():
			suicide = True

		index = self.characters.index(character)
		self.characters.pop(index)



		tile = character.get_tile()
		character.set_coordinates(None)
		tile.remove_character()
		self.gui.remove_character(character) #Remove icon

		self.gui.update_log(character.get_name()+ " died.")

		if suicide:
			self.turn -= 1 #The turn ends but the players move forward in position
			self.gui.parse_trigger("End turn")
		elif index < self.turn: #Keep the turn on the active character if a previous character is killed
			self.turn -= 1

		self.gui.update_stats()

	#Kill all dead characters and count how many of each team are alive
	def update_game(self):
		players = 0
		enemies = 0

		for char in self.characters:
			if char.get_hp() <= 0:
				self.kill_character(char)

		#Two loops because items are popped from the first one
		for char in self.characters:
			if char.is_controllable():
				players += 1
			else:
				enemies += 1

		#Check if game ends
		if players < 1:
			self.gui.parse_trigger("End L")
		elif enemies < 1 :
			self.gui.parse_trigger("End W")

		self.gui.update_stats()
