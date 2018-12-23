from PyQt5 import QtWidgets, QtCore, QtGui

from game import Game
from image import Image
from exceptions import *
from player import Player
from brute import Brute
from runner import Runner
from ranger import Ranger
from attack import Attack
import os

#Created the playable game based on a given file

class SaveParser(object):

	def __init__ (self):
		self.save_comments = None
		self.game = None
		self.characters = []
		self.map_path = None
		self.tile_map = dict() #key = (R,G,B), value = (content, graphic)
		self.game_index = 0
		self.game_paths = []

		#Read map initialisation file to match pixel values and properties
		try:
			map_map = open("maps/maps.ini")
			for line in map_map:
				if line[0] == '#':
					pass
				else:
					self.parse_map_ini(self.tile_map, line)

			if len(self.tile_map) == 0:
				raise CorruptedSaveError("Map initialisation file is empty.")
		
		except OSError:
			raise CorruptedSaveError("Map initialisation file is corrupt.")
		finally:
			if map_map:
				map_map.close()
			else:
				return

	def get_game(self):
		return self.game

	def read_save(self, path):
		try:
			save = open(path)

			if save == None:
				print("Could not open {}".format(path))

			current_line = save.readline()
			header_parts = current_line.split(" ")

			#Check header
			if header_parts[0] != "CC":
			    raise CorruptedSaveError("Unknown file type")

			if header_parts[1].strip().lower() != 'save':
			    raise CorruptedSaveError("File is not a save file")
			header_read = True

			for line in save:
				if line[0] == '#':
					content = ''
					block_header = save.readline() #Excluding #in first position
					block_header = block_header.split(":")
					block_name = block_header[0].strip()
					block_name = block_name.lower()

					if block_name == "information":
						while content[0:2] != '/#':
							content = save.readline()
							self.parse_save_information(content)
						info_read = True

					if block_name == "games":
						while content[0:2] != '/#':
							content = save.readline()
							self.parse_games(content)
						games_read = True

					if block_name == "player":
						player = Player()
						while content[0:2] != '/#':
							content = save.readline()
							self.parse_character(content, player)
						self.parse_folder(player)
						if self.char_ok(player):	
							self.characters.append(player)
						else:
							raise CorruptedSaveError("File has corrupt player information")

			#find path of the next game
			next_game_path = "games/{}.txt".format(self.game_paths[self.game_index])

			self.generate_map(next_game_path)

		except OSError:
			raise CorruptedSaveError("Reading the save data failed.")

		finally:
			if save:
				save.close()
			else:
				return

	def save_save(self, path):
		pass


	def generate_map(self,path):

		info_read = False
		header_read = False
		current_line = ''	
		content = ''
		
		#Read map file
		try:
			map_file = open(path)

			if map_file == None:
				print("Could not open {}".format(path))

			current_line = map_file.readline()
			header_parts = current_line.split(" ")

			#Check header
			if header_parts[0] != "CC":
			    raise CorruptedSaveError("Unknown file type")

			if header_parts[1].strip().lower() != 'game':
			    raise CorruptedSaveError("File is not a game")
			header_read = True

			for line in map_file:
				if line[0] == '#':
					content = ''
					block_header = map_file.readline() #Excluding #in first position
					block_header = block_header.split(":")
					block_name = block_header[0].strip()
					block_name = block_name.lower()

					if block_name == "information":
						while content[0:2] != '/#':
							content = map_file.readline()
							self.parse_game_information(content)
						info_read = True

					if block_name == "enemy":
						if len(block_header) == 1: #Make sure that all enemies have an AI
							raise CorruptedSaveError("An enemy is missing behaviour")
						enemy = self.parse_enemy_type(block_header[1])
						while content[0:2] != '/#':
							content = map_file.readline()
							self.parse_character(content, enemy)
						self.parse_folder(enemy)
						if self.char_ok(enemy):	
							self.characters.append(enemy)
						else:
							raise CorruptedSaveError("File has corrupt player information")


			#Sort characters based on initiative
			self.characters = sorted(self.characters, key=lambda character: character.get_initiative())
			self.characters.reverse()

			if not self.map_path:
				raise CorruptedSaveError("Save is missing map")

			im = Image(self.map_path)
			width = im.get_width()
			height = im.get_height()
			
			#Create game
			self.game =  Game(width, height, self.characters,self.mapname)
			for y in range(height):
				for x in range(width):
					pix_val = im.get_pixel(x,y)
					[blocks_vision, blocks_movement, graphics] = self.determine_tile(pix_val)
					self.game.set_tile_contents((x,y),blocks_vision, blocks_movement, graphics)

			return

		except OSError:
			raise CorruptedSaveError("Reading the save data failed.")

		finally:
			if map_file:
				map_file.close()
			else:
				return

	#Determine map contents based on pixel value
	def determine_tile(self,pix_val):
		
		try:
			value = self.tile_map[pix_val]
			blocks_vision = value[0]
			blocks_movement = value[1]
			graphics = value[2]
			
		#Default to empty ground
		except KeyError:
			blocks_vision = False
			blocks_movement = False
			graphics = None

		return [blocks_vision, blocks_movement, graphics]

	#Determine tile types for each pixel value
	def parse_map_ini(self, dictionary, line):
		line_content = line.split(":")
		if len(line_content) < 6:
			return

		red = int(line_content[0].strip())
		green = int(line_content[1].strip())
		blue = int(line_content[2].strip())

		tile_blocks_vision = line_content[3].strip() == "1"
		tile_blocks_movement = line_content[4].strip() == "1"

		tile_graphic = line_content[5].strip()
		tile_graphic = tile_graphic.upper()
		if tile_graphic == "NONE":
			tile_graphic = None

		key = (red, green, blue)
		value = (tile_blocks_vision, tile_blocks_movement, tile_graphic)

		dictionary[key] = value

	def parse_save_information(self,line):
		content = line.split(":")
		if len(content) < 2:
			return

		key = content[0].strip()
		key = key.lower()
		data = content[1].strip()

		if key=="index":
			self.game_index = int(data)

	def parse_games(self, line):
		content = line.split(":")
		if len(content) < 2:
			return

		key = content[0].strip()
		key = key.lower()
		data = content[1].strip()

		if key=="name":
			self.game_paths.append(data)
			

	#Determine header information
	def parse_game_information(self,line):
		content = line.split(":")
		if len(content) < 2:
			return

		key = content[0].strip()
		key = key.lower()
		data = content[1].strip()

		if key=="map":
			self.mapname = data
			self.map_path = "maps/{}.bmp".format(data)

	#Determine character information
	def parse_character(self,line,character):
		content = line.split(":")
		if len(content) < 2:
			return

		content = list(map(lambda s: s.strip(),content))
		key = content[0]
		key = key.lower()


		if key == 'name':
			character.set_name(content[1])

		#Can set hp other than max hp
		elif key == 'hp':
			character.set_hp_max(int(content[1]))
			if len(content)>2:
				character.set_hp(int(content[2]))
			else:
				character.set_hp(int(content[1]))

		elif key == 'mp':
			character.set_mp_max(int(content[1]))
			if len(content)>2:
				character.set_mp(int(content[2]))
			else:
				character.set_mp(int(content[1]))

		elif key == 'ap':
			character.set_ap_max(int(content[1]))
			if len(content)>2:
				character.set_ap(int(content[2]))
			else:
				character.set_ap(int(content[1]))

		elif key == 'init':
			character.set_initiative(int(content[1]))

		#Level affects available attacks, only cosmetic for enemies
		elif key == 'level':
			character.set_level(int(content[1]))

	def parse_enemy_type(self, line):
		content = line.strip()
		content = content.lower()

		if content == "brute":
			return Brute()
		elif content == "runner":
			return Runner()
		elif content == "ranger":
			return Ranger()
		else:
			raise CorruptedSaveError("Save file has unknown enemy types")

	#Find attacks  in character folder
	def parse_folder(self,char):
		name = char.get_name().lower()
		path = "characters/{}/attacks".format(name)
		index = 0
		for file in os.listdir(path):
			if file.endswith(".txt"):
				attack = self.parse_attack("characters/{}/attacks/{}".format(name,file))
				char.add_attack(attack, index)
				index += 1

	#Determine attack parameters
	def parse_attack(self, path):

		damage = 0
		cost = 0
		max_range = 0

		data = None
		effect = None

		try:
			data = open(path)
		except OSError:
			raise CorruptedSaveError("Could not open attack file path")
		else:
			name = data.readline().strip()

			for line in data:
				content = line.split(":")

				if len(content) > 1:
					content = list(map(lambda s: s.strip(),content))
					key = content[0]
					key = key.lower()

					if key == "damage":
						damage = (int(content[1]),int(content[2]))
					elif key == "cost":
						cost = int(content[1])
					elif key == "range":
						max_range = int(content[1])
					else:
						effect = [key, int(content[1])]


		finally:
			if data:
				data.close()
		

		if damage == 0 or cost == 0 or max_range == 0:
			raise CorruptedSaveError(path+ " Has corrupted attack information")

		return Attack(name, cost, max_range, damage, effect)

	#Check id character has required attributes
	def char_ok(self, char):
		if char.get_name() and char.get_hp_max() and char.get_ap_max() and char.get_mp_max():
			return True
		else:
			return False
