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
import copy
#Created the playable game based on a given file

class SaveParser(object):

	def __init__ (self):
		self.save_comments = None
		self.map_path = None
		self.tile_map = dict() #key = (R,G,B), value = (content, graphic)
		self.game_index = 0

		#list all games and choose one to be loaded based on the game index
		#game includes map name and list of enemies  in (name, level) format
		self.games = []
		self.mapname = ""
		self.enemies = []
		self.players = []

		#Read all enemy types into memory
		self.all_enemies = dict()

		try:
			enemy_stats = open("characters/enemy_stats.txt")

			if enemy_stats == None:
				print("Could not open enemy stat file")

			current_line = enemy_stats.readline()
			header_parts = current_line.split(" ")

			#Check header
			if header_parts[0] != "CC":
			    raise CorruptedSaveError("Unknown enemy stat file type")

			if header_parts[1].strip().lower() != 'enemy':
			    raise CorruptedSaveError("File is not a enemy stat file")
			header_read = True

			
			for line in enemy_stats:
				if line[0] == '#':
					content = ''
					block_header = enemy_stats.readline() #Excluding #in first position
					block_header = block_header.split(":")

					if len(block_header) == 1:
						name = block_header[0].strip().lower()

						content = enemy_stats.readline()
						content = content.split(":")
						enemy_type = content[0].strip().lower()

						num_level = len(content)-1 #Number of different levels for enemies

						levels = [] #store levels in temporary vector to access the keys in second loop

						#Add correct amount of enemies to the dictionary
						for i in range(num_level):
							enemy = self.parse_enemy_type(enemy_type)
							level = int(content[i+1])
							levels.append(level)

							enemy.set_name(name)
							enemy.set_level(level)

							key = (name, level)
							self.all_enemies[key] = enemy


						while content[0:2] != '/#':
							content = enemy_stats.readline()
							#Add stats for each enemy
							for i in range(num_level):
								self.parse_character(content, self.all_enemies[(name, levels[i])], i)

						#Currently not checkin if all enemies are ok

			if len(self.all_enemies) == 0:
				raise CorruptedSaveError("Enemy stat file is empty.")
		
		except OSError:
			raise CorruptedSaveError("Enemy stat file is corrupt.")
		finally:
			if enemy_stats:
				enemy_stats.close()
			else:
				return

		#Read map initialisation file to match pixel values and properties
		try:
			map_map = open("maps/maps.txt")
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

	def next_game(self):
		if self.game_index < (len(self.games)-1):
			self.game_index += 1

	def get_num_games(self):
		return len(self.games)

	def get_game(self):
		#Load next game
		next_game = self.games[self.game_index]
		
		characters = []

		#Characters are copies to not preserve their stats or position
		for player in self.players:
			characters.append(copy.copy(player))

		enemies = next_game[1]
		self.mapname = next_game[0]

		for i in enemies:
			enemy = self.all_enemies[i]
			if self.char_ok(enemy):	
				characters.append(copy.copy(enemy))
			else:
				raise CorruptedSaveError("File has corrupt player information")


		#Sort characters based on initiative
		characters = sorted(characters, key=lambda character: character.get_initiative())
		characters.reverse()

		map_path = "maps/{}.bmp".format(self.mapname)

		im = Image(map_path)
		width = im.get_width()
		height = im.get_height()
		

		#Create game
		game =  Game(width, height, characters, self.mapname)
		for y in range(height):
			for x in range(width):
				pix_val = im.get_pixel(x,y)
				[blocks_vision, blocks_movement, graphics] = self.determine_tile(pix_val)
				game.set_tile_contents((x,y),blocks_vision, blocks_movement, graphics)

		return game

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

					if block_name == "game":
						#reset map name and enemy list before adding them to next entry in games list
						self.mapname = ""
						self.enemies = []
						while content[0:2] != '/#':
							content = save.readline()
							self.parse_game(content)

						self.games.append((self.mapname, self.enemies))

						games_read = True #games read is true if even one game is read

					if block_name == "player":
						player = Player()
						while content[0:2] != '/#':
							content = save.readline()
							self.parse_character(content, player,0)
						if self.char_ok(player):	
							self.players.append(player)
						else:
							raise CorruptedSaveError("File has corrupt player information")


		except OSError:
			raise CorruptedSaveError("Reading the save data failed.")

		finally:
			if save:
				save.close()
			else:
				return

	def save_save(self, path):
		pass

	
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

	def parse_game(self, line):
		content = line.split(":")
		if len(content) < 2:
			return

		content = list(map(lambda s: s.strip(),content))
		key = content[0]
		key = key.lower()

		if key == "map":
			self.mapname = content[1].lower()

		elif key == "enemy":
			name = content[1].lower()
			level = int(content[2])
			self.enemies.append((name, level))


	#Determine character information
	#level is used to read info about enemies
	def parse_character(self,line,character, level):
		content = line.split(":")
		if len(content) < 2 + level:
			return

		content = list(map(lambda s: s.strip(),content))
		key = content[0]
		key = key.lower()


		if key == 'name':
			character.set_name(content[1+level])

		#Can set hp other than max hp
		elif key == 'hp':
			character.set_hp_max(int(content[1+level]))
			character.set_hp(int(content[1+level]))

		elif key == 'mp':
			character.set_mp_max(int(content[1+level]))
			character.set_mp(int(content[1+level]))

		elif key == 'ap':
			character.set_ap_max(int(content[1+level]))
			character.set_ap(int(content[1+level]))

		elif key == 'init':
			character.set_initiative(int(content[1+level]))

		#Level affects available attacks
		elif key == 'level':
			character.set_level(int(content[1+level]))

		elif key == 'attack':
			attack = self.parse_attack("attacks/{}.txt".format(content[1+level]))
			character.add_attack(attack)

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
			raise CorruptedSaveError("Could not open attack file path:{}".format(path))
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
