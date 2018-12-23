from enemy import Enemy

#Enemy that gets into melee distance and tries to hide after every attack

class Runner(Enemy):
	def init(self):
		super().__init__()

	def make_action(self):
		if self.animating: #Don't make new actions while animation is playing
			return


		target = self.get_closest_player()
		targetpos = target.get_coordinates()

		#Try to move to target
		if self.counter == 0:

			self.move_towards(targetpos)
			self.counter += 1

		#Try to attack target
		elif self.counter == 1:

			#Choose optimal attack
			attack = self.select_attack(targetpos)

			#Use attack if one is applicable
			if attack:
				self.attack(target, attack)
			
			#Keep using attacks until out of AP
			else:
				self.counter += 1

		#End turn
		elif self.counter == 2:

			target = self.hide_far()
			if target:
				self.move(target)
			self.counter += 1

		elif self.counter == 3:

			self.counter = 0
			self.busy = False

		self.game.update_game()