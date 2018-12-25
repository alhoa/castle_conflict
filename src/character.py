from algorithms import find_route, find_los, find_area

class Character():

	def __init__(self, name = None, initiative = 10, level = 1):
		self.hp_max = None
		self.ap_max = None
		self.mp_max = None
		self.hp = self.hp_max
		self.ap = self.ap_max
		self.mp = self.mp_max
		self.initiative = initiative
		self.level = level
		self.coordinates = None
		self.game = None
		self.name = name
		self.attacks = [None]*6
		self.path = []
		self.animating = False
		self.face = 1

		#stats
		self.strength = 0     #Damage output
		self.dexterity = 0	  #Hit probability
		self.agility = 0	  #Evade chance


	def set_game(self, game):
		self.game = game
	def get_game(self):
		return self.games

	def get_face(self):
		return self.face

	def set_face(self,face):
		self.face = face

	def get_tile(self):
		return self.game.get_tile(self.coordinates)
	
	def set_coordinates(self, coords):
		self.coordinates = coords
	def get_coordinates(self):
		return self.coordinates

	def set_animating(self, val):
		self.animating = val	  #Value is set to true in this function and to false in gui
	def is_animating(self):
		return self.is_animating

	def set_path(self, pth):
		self.path = pth
	def get_path(self):
		return self.path

	def add_attack(self, attack):
		#only add attacks up to 6
		for i in range(len(self.attacks)):
			if not self.attacks[i]:
				self.attacks[i] = attack
				return

	def get_attacks(self):
		return self.attacks

	def set_level(self, val):
		self.level = val
	def get_level(self):
		return self.level

	def is_controllable(self):
		pass
		#Will return true for players and false for enemies

	def init_turn(self):
		self.game.get_gui().update_log("It is now " + self.name +"'s turn")

		#Add active status effects (poison etc.) here in the future

	def end_turn(self):
		#Replenish AP and MP at end of turn that status effects can change them on other turns
		self.ap = self.ap_max
		self.mp = self.mp_max

	def move(self, stop):

		self.path = find_route(self.game,self.coordinates,stop)

		#Check if walking to tile is possible
		if len(self.path) > self.mp:
			if self.is_controllable(): #update log only for players
				self.game.get_gui().update_log(self.name+ " cannot walk that far")
		elif len(self.path) == 0:
			if self.is_controllable():
				self.game.get_gui().update_log(self.name+ " cannot walk there")

		#If walking is possible, move character
		else:
			self.animating = True
			self.game.gui.move_character(self) #Move in gui
			self.get_tile().remove_character() #Remove from tile
			self.game.get_tile((stop[0],stop[1])).set_character(self) #Add to new tile
			self.set_coordinates((stop[0],stop[1])) #Change character parameter

			self.change_mp(-len(self.path))#Remove MP

		self.game.get_gui().update_stats()
		self.game.update_game()


	def __str__(self):
		text = '{}, hp: {}, ap: {}, mp: {}'.format(self.get_name(), self.get_hp(), self.get_ap(), self.get_mp())
		return text

	#carry out additional attack effects, same for both player and enemy
	def parse_attack_effect(self, attack, char):
		if attack.get_effect() == None:
			return

		name = attack.get_effect()[0]
		value = attack.get_effect()[1]

		if name == "ap":
			char.set_ap(char.get_ap()+value)
			self.game.gui.update_log("{} removed {} AP from {}!".format(self.name, str(abs(value)), char.get_name()))
		elif name == "mp":
			char.set_mp(char.get_mp()+value)
			self.game.gui.update_log("{} removed {} MP from {}!".format(self.name, str(abs(value)), char.get_name()))


	# Get and set functions for all statistics

	def get_initiative(self):
		return self.initiative
	def set_initiative(self, initiative):
		self.initiative = initiative

	def get_name(self):
		return self.name
	def set_name(self, name):
		self.name = name


	def get_hp(self):
		return self.hp
	def set_hp(self, hp):
		self.hp = hp

	def get_ap(self):
		return self.ap
	def set_ap(self, ap):
		self.ap = ap

	def get_mp(self):
		return self.mp
	def set_mp(self, mp):
		self.mp = mp

	def get_hp_max(self):
		return self.hp_max
	def set_hp_max(self, hp):
		self.hp_max = hp

	def get_ap_max(self):
		return self.ap_max
	def set_ap_max(self, ap):
		self.ap_max = ap

	def get_mp_max(self):
		return self.mp_max
	def set_mp_max(self, mp):
		self.mp_max = mp

	def get_strength(self):
		return self.strength
	def set_strength(self, val):
		self.strength = val
	
	def get_dexterity(self):
		return self.dexterity
	def set_dexterity(self, val):
		self.dexterity = val

	def get_agility(self):
		return self.agility
	def set_agility(self, val):
		self.agility = val

	def change_hp(self,val):
		self.hp += val

	def change_ap(self,val):
		self.ap += val

	def change_mp(self,val):
		self.mp += val

# Ends here