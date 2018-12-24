#!/usr/bin/python3

import sys
from PyQt5 import QtWidgets, QtGui

from saveparser import SaveParser
from exceptions import *
from gui import GUI
import mainwindow


def main():

	global app
	app = QtWidgets.QApplication(sys.argv)
	main = mainwindow.MainWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
