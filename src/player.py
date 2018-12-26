from character import Character
from algorithms import find_route, find_los, find_area


class Player(Character):

	def __init__(self):
		super().__init__()
		self.controllable = True
		self.active_attack = None
		self.attackable_coords = []
		self.xp = 0
		self.stored_xp = 0

		#Points to unock stuff with
		self.spell_points = 0
		self.stat_points = 0

	def get_xp(self):
		return self.xp
	def set_xp(self, val):
		self.xp = val

	def get_stat_points(self):
		return self.stat_points
	def set_stat_points(self, val):
		self.stat_points = val

	def get_spell_points(self):
		return self.spell_points
	def set_spell_points(self, val):
		self.spell_points = val

	def store_xp(self):
		self.stored_xp += self.xp
	def get_stored_xp(self):
		return self.stored_xp

	def get_xp_for_next_lvl(self):
		return int(100*(1.1**self.level))

	def is_controllable(self):
		return self.controllable

	#Choose attack based on selected index and highlight possible targets
	def choose_target(self, index):
		attack = self.attacks[index]
		if attack == None:
			return

		if self.ap >= attack.get_cost():
			self.active_attack = attack
			range = self.active_attack.get_range()
			self.attackable_coords = find_los(self.game,self.coordinates,range)
		else:
			self.game.gui.update_log("Not enough AP")

	#Cancel target selection
	def cancel_attack(self):
		self.active_attack = None
		self.attackable_coords = []

	def get_attackable_coordinates(self):
		return self.attackable_coords

	#Deal damage and status effects. Doesn't check AP requirements
	def attack(self, target):
		if target in self.attackable_coords:
			char = self.game.get_tile(target).get_character()
			self.ap -= self.active_attack.get_cost()

			#Define turn direction
			x = target[0]-self.coordinates[0]
			y = target[1]-self.coordinates[1]
			self.game.gui.get_character_graphics(self).turn(x, y)

			if char:
				dmg = self.active_attack.calculate_damage()
				self.add_xp(dmg*5)#Temporary xp system, allows farming with teammates
				char.set_hp(char.get_hp()-dmg)
				self.parse_attack_effect(self.active_attack, char)
				self.game.gui.update_log("{} attacked {} with {} for {} damage!".format(self.name, char.get_name(), self.active_attack.get_name(), str(dmg)))
				self.game.gui.add_hitsplat(target,dmg)
			else:
				self.game.gui.update_log("{} Used {} on square {}".format(self.name, self.active_attack.get_name(), str(target)))
				self.game.gui.add_hitsplat(target,0)
		else:
			self.game.gui.update_log("You can't attack that square")

		self.game.update_game()
		self.cancel_attack()

	def add_xp(self, val):
		self.xp += val

		required_xp = self.get_xp_for_next_lvl()
		#Check if leveled up
		if (self.xp+self.stored_xp)>=required_xp:
			self.xp = self.xp+self.stored_xp-required_xp
			self.stored_xp = 0

			self.level += 1
			self.stat_points += 5
			self.spell_points += 1

			self.game.gui.update_log("{} gained a level!".format(self.name))

			
	def increase_strength(self):
		if self.stat_points >= 1:
			self.stat_points -= 1
			self.strength += 1

	def increase_dexterity(self):
		if self.stat_points >= 1:
			self.stat_points -= 1
			self.dexterity += 1

	def increase_agility(self):
		if self.stat_points >= 1:
			self.stat_points -= 1
			self.agility += 1

	def increase_hp(self):
		if self.stat_points >= 1:
			self.stat_points -= 1
			self.hp_max += 1
			self.hp = self.hp_max

	def increase_ap(self):
		if self.stat_points >= 10:
			self.stat_points -= 10
			self.ap_max += 1
			self.ap = self.ap_max

	def increase_mp(self):
		if self.stat_points >= 10:
			self.stat_points -= 10
			self.mp_max += 1
			self.mp = self.mp_max

	def increase_initiative(self):
		if self.stat_points >= 1:
			self.stat_points -= 1
			self.initiative += 5
