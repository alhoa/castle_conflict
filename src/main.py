#!/usr/bin/python3

import sys
from PyQt5 import QtWidgets, QtGui

from saveparser import SaveParser
from exceptions import *
from gui import GUI


def main():

	global app
	app = QtWidgets.QApplication(sys.argv)

	#Show dialog window to choose save file
	dialog = QtWidgets.QFileDialog()
	dialog.setDirectory("saves/")
	fname = dialog.getOpenFileName(None, 'Castle Conflict - Choose save file')

	save_path = fname[0]
	save = None
	
	try:
		parser = SaveParser()
		parser.read_save(save_path)
		game = parser.get_game()
		gui = GUI(game)
	except CorruptedSaveError as msg:
		print(msg)
		sys.exit()


	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
