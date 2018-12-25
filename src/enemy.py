from character import Character
import time
from algorithms import *

class Enemy(Character):

	def __init__(self):
		super().__init__()
		self.controllable = False
		self.busy = True
		self.counter = 0 #To put actions in order

	def is_controllable(self):
		return self.controllable

	def is_busy(self):
		return self.busy

	def make_action(self):
		#Implement in subclasses
		pass
		
	def init_turn(self):
		self.game.get_gui().update_log("It is now " + self.name +"'s turn")
		self.busy = True



	#Find player closest to the enemy
	def get_closest_player(self):
		characters = self.game.get_characters()

		mindist = 10000
		target = None

		for character in characters:
			if character.is_controllable():
				dist = get_distance(self.get_coordinates(), character.get_coordinates())

				if dist < mindist:
					mindist = dist
					target = character

		return target

	#Move towards a target. Use only for moving towars squares that cannot be stepped on ie. players or enemys
	def move_towards(self, target):

		#Check if already next to player
		if get_distance(self.coordinates, target) == 1:
			return

		#Otherwise walk to the nearest square next to the target
		move_target = closest_coordinate(self.game, self.coordinates, target)

		path = find_route(self.game,self.coordinates,move_target)

		#If no path is found, don't move
		if len(path) == 0:
			return

		if len(path) < self.mp:
			self.move(path[-1])

		else:
			self.move(path[self.mp-1])

	#AP check done elsewhere, this only deals damage and status effects
	def attack(self, target, attack):

		attackable_coords = find_los(self.game,self.coordinates,attack.get_range())

		targetpos = target.get_coordinates()

		#Attack target if possible
		if targetpos in attackable_coords:

			self.game.gui.get_character_graphics(self).turn(1, 1)

			self.ap -= attack.get_cost()
			dmg = attack.calculate_damage()

			#Deal the damage
			target.set_hp(target.get_hp()-dmg)
			self.parse_attack_effect(attack, target)
			self.game.gui.update_log("{} attacked {} with {} for {} damage!".format(self.name, target.get_name(), attack.get_name(), str(dmg)))
			self.game.gui.add_hitsplat(targetpos,dmg)

		#In case no attack is possible, move to next AI step
		else:
			self.counter += 1			

	#Find all tiles that the character can walk to
	def get_walkable_tiles(self):
		#Take squares inside mp circle
		inits = find_area(self.game, self.get_coordinates(), self.mp)

		#initialize with own location, because the enemy can always remain stationary
		walkable = [self.get_coordinates()]

		for tile in inits:
			route = find_route(self.game, self.get_coordinates(), tile)
			if len(route) <= self.mp and len(route)>0:
				walkable.append(tile)


		return walkable

	#Find tiles that are hidden from the most amount of players
	def get_hidden_tiles(self):

		tiles = self.get_walkable_tiles()
		maxhidden = 0

		targets = []

		for tile in tiles:
			hidden_num = hidden(self.game, tile, self)
			if hidden_num > maxhidden:
				maxhidden = hidden_num
				targets = [tile]          #Remove all tiles hidden from lesser players
			elif hidden_num == maxhidden:
				targets.append(tile)

		return targets

	#Find fartherst hidden squate
	def hide_far(self):

		targets = self.get_hidden_tiles()

		#Select target that is furthest away
		maxdist = -1

		for tile in targets:
			dist = len(find_route(self.game, self.get_coordinates(), tile))
			if dist > maxdist:
				maxdist = dist
				target = tile

		return target

	#Find nearest hidden square
	def hide_near(self):

		targets = self.get_hidden_tiles()

		#Select target that is nearest
		mindist = 100

		for tile in targets:
			dist = len(find_route(self.game, self.get_coordinates(), tile))
			if dist < mindist:
				mindist = dist
				target = tile

		return target

	#Return highest range of attacks
	def find_max_attack_dist(self):
		maxrange = 0
		for attack in self.attacks:
			if attack:
				range = attack.get_range()
				if range > maxrange:
					maxrange = range

		return maxrange

	#Find all tiles that can be attacked after walking
	def find_attackable_tiles(self, target, dist):

		inits = self.get_walkable_tiles()

		maxwalk = self.get_mp()

		tile = None

		for coords in inits:
			walk_dist = len(find_route(self.game, self.get_coordinates(), coords))
			attackable_tiles = find_los(self.game, coords, dist)
			if target in attackable_tiles and walk_dist < maxwalk:
				maxwalk = walk_dist
				tile = coords

		return tile

	#Choose attack for maimal damage output
	def select_attack(self, target):

		distance = get_distance(self.get_coordinates(), target)
		max_dpa = 0
		chosen = None

		for attack in self.attacks:
			if attack:
				dpa = int(10*attack.get_max_damage()/attack.get_cost())
				if dpa > max_dpa and attack.get_range() >= distance and self.ap >= attack.get_cost():
					chosen = attack

		return chosen

	#Function to choose between multiple targets
	def find_target_player(self):
		maxhp = 10000
		target = None

		players = self.game.get_players()
		for player in players:
			in_range = self.find_max_attack_dist() >= get_distance(self.get_coordinates(), player.get_coordinates())
			if line_free(self.game, self.get_coordinates(), player.get_coordinates()) and in_range:
				if player.get_hp() < maxhp:
					hp = player.get_hp()
					target = player


		if not target:
			target = self.get_closest_player()

		return target

