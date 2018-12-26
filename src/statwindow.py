from PyQt5 import QtWidgets, QtCore, QtGui
from exceptions import *

import random

#This class handles all graphical elements of the game

class StatWindow(QtWidgets.QMainWindow):

	def __init__(self, char, attacks):
		super().__init__()
		
		self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
		self.layout = QtWidgets.QGridLayout() #Use grid layout
		self.centralWidget().setLayout(self.layout)

		self.char = char
		self.attacks = attacks

		self.WIDTH = 360

		self.setGeometry(0, 0, self.WIDTH, 360) #window size
		#Initialize graphical elements
		self.init_grid()
		self.init_exit_button()
		self.init_attack_buttons()

		self.show()


	def init_grid(self):

		self.label_group = QtWidgets.QGridLayout()

		for i in range(6):
			self.label_group.setColumnMinimumWidth(i, self.WIDTH/6)

		self.nameval_label = QtWidgets.QLabel(self.char.get_name())
		self.label_group.addWidget(self.nameval_label, 0, 0,1,1)

		self.level_label = QtWidgets.QLabel("Level:")
		self.label_group.addWidget(self.level_label, 0,1,1,1)

		self.level_val_label = QtWidgets.QLabel(str(self.char.get_level()))
		self.label_group.addWidget(self.level_val_label,0,2,1,1)

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

		self.ap_label = QtWidgets.QLabel("Total xp:")
		self.label_group.addWidget(self.ap_label,0,3,1,1)

		self.apval_label = QtWidgets.QLabel(str(self.char.get_stored_xp()))
		self.label_group.addWidget(self.apval_label,0,4,1,1)

		self.str_label = QtWidgets.QLabel("Strength:")
		self.label_group.addWidget(self.str_label,2,0,1,1)

		self.strval_label = QtWidgets.QLabel(str(self.char.get_strength()))
		self.label_group.addWidget(self.strval_label,2,1,1,1)

		self.dex_label = QtWidgets.QLabel("Dexterity:")
		self.label_group.addWidget(self.dex_label,2,2,1,1)

		self.dexval_label = QtWidgets.QLabel(str(self.char.get_dexterity()))
		self.label_group.addWidget(self.dexval_label,2,3,1,1)

		self.agi_label = QtWidgets.QLabel("Agility:")
		self.label_group.addWidget(self.agi_label,2,4,1,1)

		self.agival_label = QtWidgets.QLabel(str(self.char.get_agility()))
		self.label_group.addWidget(self.agival_label,2,5,1,1)

		self.stat_points_label = QtWidgets.QLabel("Stat points available:")
		self.label_group.addWidget(self.stat_points_label ,4,0,1,2)

		self.stat_val_label = QtWidgets.QLabel(str(self.char.get_stat_points()))
		self.label_group.addWidget(self.stat_val_label,4,2,1,1)

		self.spell_points_label = QtWidgets.QLabel("Spell points available:")
		self.label_group.addWidget(self.spell_points_label,4,3,1,2)

		self.spell_val_label = QtWidgets.QLabel(str(self.char.get_spell_points()))
		self.label_group.addWidget(self.spell_val_label,4,5,1,1)

		self.str_up = QtWidgets.QPushButton("+")
		self.str_up.setToolTip("Add points to STR")
		self.str_up.clicked.connect(self.increase_strength)
		self.label_group.addWidget(self.str_up, 3, 1, 1, 1)

		self.dex_up = QtWidgets.QPushButton("+")
		self.dex_up.setToolTip("Add points to DEX")
		self.dex_up.clicked.connect(self.increase_dexterity)
		self.label_group.addWidget(self.dex_up, 3, 3, 1, 1)

		self.agi_up = QtWidgets.QPushButton("+")
		self.agi_up.setToolTip("Add points to AGI")
		self.agi_up.clicked.connect(self.increase_agility)
		self.label_group.addWidget(self.agi_up, 3, 5, 1, 1)

		self.label_box = QtWidgets.QGroupBox()
		self.label_box.setLayout(self.label_group)
		self.layout.addWidget(self.label_box, 0,0,1,1)


	def init_attack_buttons(self):

		self.button_group = QtWidgets.QGridLayout()

		x = 0
		y = 0

		for key in self.attacks:
			name = self.attacks[key].get_name().lower().replace(" ", "_")
			path = "attacks/{}.png".format(name)
			icon = QtGui.QIcon(QtGui.QPixmap(path))
			btn = QtWidgets.QPushButton(icon,"")
			btn.setIconSize(QtCore.QSize(50,50))
			btn.setToolTip(str(self.attacks[key]))

			#Only press buttons that the character does not have
			if self.attacks[key] in self.char.get_attacks():
				btn.setEnabled(False)
			
			btn.clicked.connect(lambda state, x=key: self.unlock_attack(x))
			self.button_group.addWidget(btn, y, x, 1, 1)

			x += 1
			if x > 6:
				x = 0
				y += 1

		self.group_box = QtWidgets.QGroupBox()
		self.group_box.setLayout(self.button_group)
		self.layout.addWidget(self.group_box, 1,0,1,1)

	def init_exit_button(self):

		start_icon = QtGui.QIcon(QtGui.QPixmap("graphics/arrow.png"))
		start_btn = QtWidgets.QPushButton(start_icon,"")
		start_btn.setIconSize(QtCore.QSize(50,50))
		start_btn.setToolTip("Close")
		start_btn.clicked.connect(lambda: self.parse_trigger("Exit"))

		self.layout.addWidget(start_btn, 2,0,1,1)	

	def parse_trigger(self,msg,index=-1):

		if type(msg).__name__=='str':
			message = str(msg)
		else:
			message = msg.text()

		if message == "Exit": #Parse contents of message
			self.close()

	def increase_strength(self):
		self.char.increase_strength()
		self.strval_label.setText(str(self.char.get_strength()))
		self.stat_val_label.setText(str(self.char.get_stat_points()))

	def increase_dexterity(self):
		self.char.increase_dexterity()
		self.dexval_label.setText(str(self.char.get_dexterity()))
		self.stat_val_label.setText(str(self.char.get_stat_points()))

	def increase_agility(self):
		self.char.increase_agility()
		self.agival_label.setText(str(self.char.get_agility()))
		self.stat_val_label.setText(str(self.char.get_stat_points()))

	def unlock_attack(self, key):
		pass