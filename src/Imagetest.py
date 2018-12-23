#!/usr/bin/python3

#Test file to compare operation between PIL and my own image class


#class image:
#	def __init__(self):

from PIL import Image


with open("maps/isometric.bmp", "rb") as input:
	data = input.read()

print(len(data))

startloc = data[10]
width = data[18]
height = data[22]

realdata = data[startloc:]
print(len(realdata))
print(startloc, width, height)

#def get_pixel(self,x,y):
'''
location = startloc+3*(12+12+4)

R = realdata[location]
G = realdata[location+1]
B = realdata[location+2]
'''

#print(R,G,B)

pixels = [None] * width
for x in range(width):
	pixels[x] = [None] * height

x = 0
y = height-1
rowpos = 0

if width%4 == 0:
	rowsize = 3*width
else:
	rowsize = 3*width+4-(3*width)%4 #bmp rows are padded to nearest 4 bytes

print(rowsize)


for pos in range(len(realdata)):

	print(rowpos)

	if rowpos > 3*width-1:
		print("passed padding y:",y)
	elif rowpos%3 == 0:
		B = realdata[pos]
	elif rowpos%3 == 1:
		G = realdata[pos]
	elif rowpos%3 == 2:
		R = realdata[pos]
		pixels[x][y] = (R,G,B)

		print(R,G,B)

		x += 1
		if x >= width:
			x = 0
			y -= 1
			print("New row")

	if rowpos >= rowsize-1:
		rowpos = 0
	else:
		rowpos += 1
	
im = Image.open("maps/isometric.bmp")


for x in range(width):
	print(x, "PIL:", im.getpixel((x,1)),"OWN:", pixels[x][1])