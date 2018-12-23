from vertex import Vertex

#Finds shortest route between two points
def find_route(gamearea, start, stop):
	coordinates = [] #returnable list

	if gamearea.get_tile(stop).blocks_movement(): #Return empty list is attempting to move to a blocked tile
		return coordinates	

	height = gamearea.get_height()
	width = gamearea.get_width()

	#Create a verticle for each tile in the game
	verticles = [None] * width
	for x in range(width):
		verticles[x] = [None] * height
		for y in range(height):
			tile = gamearea.get_tile((x,y))
			if not tile.blocks_movement():
				verticles[x][y] = Vertex((x,y))
			elif tile.get_coordinates() == start:
				verticles[x][y] = Vertex((x,y),0)
	
	current = verticles[start[0]][start[1]]
	current_x = start[0]
	current_y = start[1]

	#simple counter to break infinite loops in case trying to walk to an isolated tile
	counter = 0
	maxcount = height*width


	while verticles[stop[0]][stop[1]].get_visited() == False:

		#List of possible next steps
		candidates = [(current_x+1, current_y), (current_x, current_y+1), (current_x-1, current_y), (current_x, current_y-1)]

		for coord in candidates:
			#Check is tile is in walkable area
			if gamearea.in_bounds(coord) and verticles[coord[0]][coord[1]] and verticles[coord[0]][coord[1]].get_visited() == False:
				tentative_dist = verticles[current_x][current_y].get_distance() + 1
				if verticles[coord[0]][coord[1]].get_distance() > tentative_dist:
					verticles[coord[0]][coord[1]].set_distance(tentative_dist) #Replace new shorest route
					verticles[coord[0]][coord[1]].set_previous(current) #Create linked list of minimum distances


		verticles[current_x][current_y].set_visited(True)

		mindist = 100000
		for lists in verticles:
			for vertex in lists:
				if vertex and vertex.get_visited() == False and vertex.get_distance()<mindist:
					mindist = vertex.get_distance()
					current = vertex

		current_x = current.get_x()
		current_y = current.get_y()

		counter += 1
		if counter > maxcount:
			return []

	previous = verticles[stop[0]][stop[1]]

	#Follow linked lis to generate the path needed to walk
	while previous:
		if previous.get_x() != start[0] or previous.get_y() != start[1]:
			coordinates.append((previous.get_x(), previous.get_y()))
		previous = previous.get_previous()

	coordinates.reverse()

	return coordinates

#Lists tiles at a specified distance from a point
def find_area(gamearea,startloc,dist):
	x0 = startloc[0]
	y0 = startloc[1]

	coordinates = [] #Returnable group

	tiles = gamearea.get_tiles()

	for line in tiles:
		for tile in line:
			x = tile.get_coordinates()[0]
			y = tile.get_coordinates()[1]
			dx = abs(x-x0)
			dy = abs(y-y0)
			if dx+dy <= dist:
				coordinates.append((x,y))

	return coordinates

#Find all points visible at a certain distance from a specified point
def find_los(gamearea, startloc, dist):

	init = find_area(gamearea, startloc, dist)

	coordinates = []

	for coord in init:
		if line_free(gamearea, startloc,coord):
			coordinates.append(coord)

	return coordinates

#Returns a list a tiles connecting two points
def bressenham(x0,y0,x1,y1):

	coordinates = []

	#if distance = 0, return starting point
	if x0 == x1 and y0 == y1:
		return [(x0,y0)]

	#Change in coordinates to determine operating octant
	dx = x1-x0
	dy = y1-y0

	error = 0

	#The same algorithm can be used if x and y have the same sign
	if dx <= 0 and dy <= 0:
		#Flip (x0,y0) and (x1,y1)
		x2 = x1
		x1 = x0
		x0 = x2

		y2 = y1
		y1 = y0
		y0 = y2

		#Calculate new signs
		dx = x1-x0
		dy = y1-y0

	if dx >= 0 and dy >= 0:
		coordinates = [(x0,y0)]
		if dx>=dy:
			slope = abs(dy/dx)
			y= y0
			for i in range(x0+1,x1+1):
				error += slope
				if error > 0.5:
					error -= 1
					y += 1

				coordinates.append((i,y))

		else:
			slope = abs(dx/dy)
			x=x0
			for i in range(y0+1,y1+1):
				error += slope
				if error > 0.5:
					error -= 1
					x += 1

				coordinates.append((x,i))

	#The same algorithm can be used if x and y have the oppsite sign
	if dx <= 0 and dy >= 0:
		#Flip (x0,y0) and (x1,y1)
		x2 = x1
		x1 = x0
		x0 = x2

		y2 = y1
		y1 = y0
		y0 = y2

		#Calculate new signs
		dx = x1-x0
		dy = y1-y0

	if dx >= 0 and dy <= 0:
		if abs(dx)>=abs(dy):
			coordinates = [(x0,y0)]
			slope = abs(dy/dx)
			y= y0
			for i in range(x0+1,x1+1):
				error -= slope
				if error < -0.5:
					error += 1
					y -= 1

				coordinates.append((i,y))

		else:
			coordinates = [(x1,y1)]
			slope = abs(dx/dy)
			x=x1
			for i in range(y1+1,y0+1):
				error -= slope
				if error < -0.5:
					error += 1
					x -= 1

				coordinates.append((x,i))


	return coordinates

#Returns linear distance between two points
def get_distance(coords1, coords2):

	dist = abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1])

	return dist

#Finds the closest adjacent coordinate from a character to a targer tile
def closest_coordinate(gamearea, start, target):

	candidates = [(target[0]+1,target[1]), (target[0],target[1]+1), (target[0]-1,target[1]), (target[0], target[1]-1)]

	mindist = 1000
	closest_square = None

	for coords in candidates:
		if gamearea.in_bounds(coords) and gamearea.get_tile(coords).is_empty():
			dist = len(find_route(gamearea,start, coords))
			if dist < mindist:
				mindist = dist
				closest_square = coords

	return closest_square

#Check if there are obstacles in a list of coordinates
def line_free(gamearea, start, end):

	tiles = gamearea.get_tiles()
	losline = bressenham(start[0],start[1],end[0], end[1])
	visible = True

	for square in losline:
			if tiles[square[0]][square[1]].blocks_vision():
				if square == end and tiles[end[0]][end[1]].get_character():  #Must be able to attack others
					pass
				elif square != start: #Check that player doesn't block all vision
					visible = False
					break

	return visible

#Returns number of players that the tile is hidden from
def hidden(game, coords, enemy):
	hidden = 0

	for char in game.get_players():
		startloc = char.get_coordinates()

		tiles = game.get_tiles()
		losline = bressenham(startloc[0],startloc[1],coords[0], coords[1])

		for square in losline:
			if tiles[square[0]][square[1]].blocks_vision():
				if square == enemy.get_coordinates():  #character current location is ignored
					pass
				elif square != startloc: #Check that player doesn't block all vision
					hidden += 1
					break


	return hidden
	