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

		self.WIDTH = 360

		self.setGeometry(0, 0, self.WIDTH, 360) #window size
		#Initialize graphical elements
		self.init_grid()
		self.init_exit_button()

		self.show()


	def init_grid(self):

		self.label_group = QtWidgets.QGridLayout()

		for i in range(6):
			self.label_group.setColumnMinimumWidth(i, self.WIDTH/6)

		nameval_label = QtWidgets.QLabel(self.char.get_name())
		self.label_group.addWidget(nameval_label, 0, 0,1,1)

		level_label = QtWidgets.QLabel("Level:")
		self.label_group.addWidget(level_label, 0,1,1,1)

		level_val_label = QtWidgets.QLabel(str(self.char.get_level()))
		self.label_group.addWidget(level_val_label,0,2,1,1)

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
		self.label_group.addWidget(progress_bar,1,0,1,6)

		ap_label = QtWidgets.QLabel("Total xp:")
		self.label_group.addWidget(ap_label,0,3,1,1)

		apval_label = QtWidgets.QLabel(str(self.char.get_stored_xp()))
		self.label_group.addWidget(apval_label,0,4,1,1)

		str_label = QtWidgets.QLabel("Strength:")
		self.label_group.addWidget(str_label,2,0,1,1)

		strval_label = QtWidgets.QLabel(str(self.char.get_strength()))
		self.label_group.addWidget(strval_label,2,1,1,1)

		dex_label = QtWidgets.QLabel("Dexterity:")
		self.label_group.addWidget(dex_label,2,2,1,1)

		dexval_label = QtWidgets.QLabel(str(self.char.get_dexterity()))
		self.label_group.addWidget(dexval_label,2,3,1,1)

		agi_label = QtWidgets.QLabel("Agility:")
		self.label_group.addWidget(agi_label,2,4,1,1)

		agival_label = QtWidgets.QLabel(str(self.char.get_agility()))
		self.label_group.addWidget(agival_label,2,5,1,1)

		points_label = QtWidgets.QLabel("Stat points available:")
		self.label_group.addWidget(points_label,4,0,1,2)

		pointval_label = QtWidgets.QLabel(str(self.char.get_stat_points()))
		self.label_group.addWidget(pointval_label,4,2,1,1)

		points_label = QtWidgets.QLabel("Spell points available:")
		self.label_group.addWidget(points_label,4,3,1,2)

		pointval_label = QtWidgets.QLabel(str(self.char.get_spell_points()))
		self.label_group.addWidget(pointval_label,4,5,1,1)

		str_up = QtWidgets.QPushButton("+")
		str_up.setToolTip("Add points to STR")
		#start_btn.clicked.connect(lambda: self.increase_strength())
		self.label_group.addWidget(str_up, 3, 0, 1, 1)

		str_dn = QtWidgets.QPushButton("-")
		str_dn.setToolTip("Remove points from STR")
		#start_btn.clicked.connect(lambda: self.increase_strength())
		self.label_group.addWidget(str_dn, 3, 1, 1, 1)

		dex_up = QtWidgets.QPushButton("+")
		dex_up.setToolTip("Add points to DEX")
		#start_btn.clicked.connect(lambda: self.increase_strength())
		self.label_group.addWidget(dex_up, 3, 2, 1, 1)

		dex_dn = QtWidgets.QPushButton("-")
		dex_dn.setToolTip("Remove points from DEX")
		#start_btn.clicked.connect(lambda: self.increase_strength())
		self.label_group.addWidget(dex_dn, 3, 3, 1, 1)

		agi_up = QtWidgets.QPushButton("+")
		agi_up.setToolTip("Add points to AGI")
		#start_btn.clicked.connect(lambda: self.increase_strength())
		self.label_group.addWidget(agi_up, 3, 4, 1, 1)

		agi_dn = QtWidgets.QPushButton("-")
		agi_dn.setToolTip("Remove points from AGI")
		#start_btn.clicked.connect(lambda: self.increase_strength())
		self.label_group.addWidget(agi_dn, 3, 5, 1, 1)



		self.label_box = QtWidgets.QGroupBox()
		self.label_box.setLayout(self.label_group)
		self.layout.addWidget(self.label_box, 0,0,1,1)


	def init_exit_button(self):

		start_icon = QtGui.QIcon(QtGui.QPixmap("graphics/arrow.png"))
		start_btn = QtWidgets.QPushButton(start_icon,"")
		start_btn.setIconSize(QtCore.QSize(50,50))
		start_btn.setToolTip("Close")
		start_btn.clicked.connect(lambda: self.parse_trigger("Exit"))

		self.layout.addWidget(start_btn, 1,0,1,1)	

	def parse_trigger(self,msg,index=-1):

		if type(msg).__name__=='str':
			message = str(msg)
		else:
			message = msg.text()

		if message == "Exit": #Parse contents of message
			self.close()
