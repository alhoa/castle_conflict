import random
#kommentti
class Attack:
	def __init__(self, name, cost,  max_range, damage, effect):
		self.name = str(name)
		self.cost = cost
		self.range = max_range
		self.damage = damage
		self.los = True      #Range modifier to be added
		self.linear = False	 #Range modifier to be added
		self.effect = effect

	def get_name(self):
		return self.name

	def get_range(self):
		return self.range

	def get_cost(self):
		return self.cost

	def get_max_damage(self):
		return self.damage[0] + self.damage[1]

	def get_effect(self):
		return self.effect
		
	def calculate_damage(self):
		dmg = self.damage[0] + random.randint(0,self.damage[1])
		return dmg

	def __str__(self):

		#Print text depends if the attack has extra effects
		if self.effect:
			text = """{}
Cost:   {}
Damage: {} + 1d{}
Range:  {}
Effect: {} {}""".format(self.name, self.cost, self.damage[0], self.damage[1], self.range, self.effect[0], self.effect[1])

		else:
			text = """{}
Cost:   {}
Damage: {} + 1d{}
Range:  {}""".format(self.name, self.cost, self.damage[0], self.damage[1], self.range)
		
		return text