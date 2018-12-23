#Class to parse bmp images

class Image:
	def __init__(self, path):
		with open(path, "rb") as input:
			data = input.read()

		#Relevant data in image header
		self.startloc = data[10]
		self.width = data[18]
		self.height = data[22]

		realdata = data[self.startloc:]

		self.pixels = [None] * self.width
		for x in range(self.width):
			self.pixels[x] = [None] * self.height

		x = 0
		y = self.height-1
		rowpos = 0

		if self.width%4 == 0:
			rowsize = 3*self.width
		else:
			rowsize = 3*self.width+4-(3*self.width)%4 #bmp rows are padded to nearest 4 bytes

		for pos in range(len(realdata)):

			if rowpos > 3*self.width-1:
				pass
			elif rowpos%3 == 0:
				B = realdata[pos]
			elif rowpos%3 == 1:
				G = realdata[pos]
			elif rowpos%3 == 2:
				R = realdata[pos]
				self.pixels[x][y] = (R,G,B)

				x += 1
				if x >= self.width:
					x = 0
					y -= 1

			if rowpos >= rowsize-1:
				rowpos = 0
			else:
				rowpos += 1

	def get_height(self):
		return self.height

	def get_width(self):
		return self.width

	def get_pixel(self,x,y):
		return self.pixels[x][y]