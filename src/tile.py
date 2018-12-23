#Specifies properties of a single tile on the map

class Tile():

	def __init__(self, coordinates):
		""" Initialize parameters of a new tile"""
		self.character = None
		self.blocks_vis = False
		self.blocks_mov = False
		self.coordinates = coordinates
		self.graphics = None

	def get_character(self):

		return self.character

	def get_coordinates(self):

		return self.coordinates

	def blocks_vision(self):

		if self.blocks_vis or self.character:
			return True
		else:
			return False

	def blocks_movement(self):
		if self.blocks_mov or self.character:
			return True
		else:
			return False

	def is_empty(self):

		if self.character == None and not(self.blocks_vis or self.blocks_mov):
			return True
		else:
			return False

	def is_graphical(self):
		if self.character == None and self.graphics:
			return True
		else:
			return False


	def is_character(self):
		if self.character:
			return True
		else:
			return False

	def set_character(self, character):
		
		if self.is_empty():
			self.character = character
			return True
		else:
			return False

	def remove_character(self):
		self.character = None

	def set_blocks_vision(self, block):
		self.blocks_vis = block

	def set_blocks_movement(self, block):
		self.blocks_mov = block

	def set_graphics(self, graphics):
		self.graphics = graphics

	def get_graphics(self):
		return self.graphics

	def is_player_spawn(self):
		if self.graphics == "PLAYER_SPAWN":
			return True
		else:
			return False

	def is_enemy_spawn(self):
		if self.graphics == "ENEMY_SPAWN":
			return True
		else:
			return False
