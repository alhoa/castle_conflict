#Single observable cell used in dijkstra's pathfinding algorithm

class Vertex():
	def __init__(self,coordinates, distance = 100001):
		self.x = coordinates[0]
		self.y =coordinates[1]
		self.visited = False
		self.distance = distance
		self.previous = None

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_distance(self):
		return self.distance

	def set_distance(self, dist):
		self.distance = dist

	def set_visited(self, value):
		self.visited = value

	def get_visited(self):
		return self.visited

	def get_previous(self):
		return self.previous

	def set_previous(self, vert):
		self.previous = vert