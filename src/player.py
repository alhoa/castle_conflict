from character import Character
from algorithms import find_route, find_los, find_area


class Player(Character):

	def __init__(self):
		super().__init__()
		self.controllable = True
		self.active_attack = None
		self.attackable_coords = []

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
			if char:
				dmg = self.active_attack.calculate_damage()
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