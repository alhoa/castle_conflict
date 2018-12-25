from PyQt5 import QtWidgets, QtCore, QtGui
from exceptions import *

import random

#This class handles all graphical elements of the game

class StatWindow(QtWidgets.QMainWindow):

	def __init__(self, char):
		super().__init__()
		
		self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
		self.layout = QtWidgets.QGridLayout() #Use grid layout
		self.centralWidget().setLayout(self.layout)

		self.char = char

		self.setGeometry(0, 0, 720, 360) #window size
		#Initialize graphical elements
		self.init_labels()
		self.init_buttons()

		self.show()


	def init_labels(self):

		self.label_group = QtWidgets.QGridLayout()

		nameval_label = QtWidgets.QLabel(self.char.get_name())
		self.label_group.addWidget(nameval_label, 1, 0,1,1)

		level_label = QtWidgets.QLabel("Level:")
		self.label_group.addWidget(level_label, 1,1,1,1)

		level_val_label = QtWidgets.QLabel(str(self.char.get_level()))
		self.label_group.addWidget(level_val_label,1,2,1,1)

		hp_label = QtWidgets.QLabel("Xp gained:")
		self.label_group.addWidget(hp_label,0,3,1,1)

		hpval_label = QtWidgets.QLabel(str(self.char.get_xp()))
		self.label_group.addWidget(hpval_label,0,4,1,1)

		no_xp_style = """
		QProgressBar{
			border: 1px solid grey;
			border-radius: 3px;
			text-align: center
		}

		QProgressBar::chunk {
			 background-color: gray;
		}
		"""

		max_xp = 100 #Value for next level
		progress_bar = QtWidgets.QProgressBar()
		progress_bar.setStyleSheet(no_xp_style)
		progress_bar.setRange(0,max_xp)
		
		progress_bar.setValue(self.char.get_stored_xp())
		self.label_group.addWidget(progress_bar,1,3,1,4)

		ap_label = QtWidgets.QLabel("Total xp:")
		self.label_group.addWidget(ap_label,0,5,1,1)

		apval_label = QtWidgets.QLabel(str(self.char.get_stored_xp()))
		self.label_group.addWidget(apval_label,0,6,1,1)

		mp_label = QtWidgets.QLabel("Loot:")
		self.label_group.addWidget(mp_label,1,7,1,1)

		mpval_label = QtWidgets.QLabel(str(self.char.get_hp()))
		self.label_group.addWidget(mpval_label,1,8,1,1)


		self.label_box = QtWidgets.QGroupBox()
		self.label_box.setLayout(self.label_group)
		self.layout.addWidget(self.label_box, 0,0,1,1)


	def init_buttons(self):

		self.button_group = QtWidgets.QGridLayout()

		start_icon = QtGui.QIcon(QtGui.QPixmap("graphics/arrow.png"))
		start_btn = QtWidgets.QPushButton(start_icon,"")
		start_btn.setIconSize(QtCore.QSize(50,50))
		start_btn.setToolTip("Close")
		start_btn.clicked.connect(lambda: self.parse_trigger("Exit"))
		self.button_group.addWidget(start_btn, 0,0,1,1)

		self.group_box = QtWidgets.QGroupBox()
		self.group_box.setLayout(self.button_group)
		self.layout.addWidget(self.group_box, 1,0,1,1)

	

	def parse_trigger(self,msg,index=-1):

		if type(msg).__name__=='str':
			message = str(msg)
		else:
			message = msg.text()

		if message == "Exit": #Parse contents of message
			self.close()
