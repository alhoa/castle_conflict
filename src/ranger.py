from enemy import Enemy

#Enemy that tries to attack from far away and hide 
#Will use melee if necessary

class Ranger(Enemy):
	def init(self):
		super().__init__()

	def make_action(self):
		if self.animating: #Don't make new actions while animation is playing
			return


		target = self.get_closest_player()
		targetpos = target.get_coordinates()


		#Try to move
		if self.counter == 0:

			#Try to move to a position where it is possible to attack
			maxrange = self.find_max_attack_dist()
			optimal_pos = self.find_attackable_tiles(targetpos, maxrange)

			#If not possible, move towrds the player
			if optimal_pos:
				self.move(optimal_pos)
			else:
				self.move_towards(targetpos)

			self.counter += 1

		#Try to attack target
		elif self.counter == 1:

			#Attack target might be a different player
			target = self.find_target_player()
			targetpos = target.get_coordinates()

			attack = self.select_attack(targetpos)

			#Use attack if one is applicable
			if attack:
				self.attack(target, attack)
			
			#Keep using attacks until out of AP
			else:
				self.counter += 1
	
		#Move away
		elif self.counter == 2:

			target = self.hide_near()
			if target:
				self.move(target)
			self.counter += 1

		#End turn
		elif self.counter == 3:



			self.counter = 0
			self.busy = False

		self.game.update_game()