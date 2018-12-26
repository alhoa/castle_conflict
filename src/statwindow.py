from PyQt5 import QtWidgets, QtCore, QtGui
from exceptions import *

import random

#This class handles all graphical elements of the game

class StatWindow(QtWidgets.QMainWindow):

	update_signal = QtCore.pyqtSignal()

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
		self.init_labels()
		self.init_stats()
		self.init_exit_button()
		self.init_attack_buttons()

		self.show()


	def init_labels(self):

		self.label_group = QtWidgets.QGridLayout()

		self.nameval_label = QtWidgets.QLabel(self.char.get_name())
		self.label_group.addWidget(self.nameval_label, 0, 0,1,1)

		self.level_label = QtWidgets.QLabel("Level:")
		self.label_group.addWidget(self.level_label, 1,0,1,1)
		self.level_val_label = QtWidgets.QLabel(str(self.char.get_level()))
		self.label_group.addWidget(self.level_val_label,1,1,1,1)

		self.xp_label = QtWidgets.QLabel("Total xp:")
		self.label_group.addWidget(self.xp_label,2,0,1,1)
		self.apval_label = QtWidgets.QLabel(str(self.char.get_stored_xp()))
		self.label_group.addWidget(self.apval_label,2,1,1,1)


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

		max_xp = self.char.get_xp_for_next_lvl()#Value for next level
		progress_bar = QtWidgets.QProgressBar()
		progress_bar.setStyleSheet(no_xp_style)
		progress_bar.setRange(0,max_xp)
		
		progress_bar.setValue(self.char.get_stored_xp())
		self.label_group.addWidget(progress_bar,3,0,1,3)

		self.stat_points_label = QtWidgets.QLabel("Stat points available:")
		self.label_group.addWidget(self.stat_points_label ,4,0,1,2)
		self.stat_val_label = QtWidgets.QLabel(str(self.char.get_stat_points()))
		self.label_group.addWidget(self.stat_val_label,4,2,1,1)

		self.spell_points_label = QtWidgets.QLabel("Spell points available:")
		self.label_group.addWidget(self.spell_points_label,5,0,1,2)
		self.spell_val_label = QtWidgets.QLabel(str(self.char.get_spell_points()))
		self.label_group.addWidget(self.spell_val_label,5,2,1,1)

		self.label_box = QtWidgets.QGroupBox()
		self.label_box.setLayout(self.label_group)
		self.layout.addWidget(self.label_box, 0,0,1,1)


	def init_stats(self):

		self.stat_group = QtWidgets.QGridLayout()

		self.hp_label = QtWidgets.QLabel("HP:")
		self.stat_group.addWidget(self.hp_label,0,0,1,1)
		self.hpval_label = QtWidgets.QLabel(str(self.char.get_hp()))
		self.stat_group.addWidget(self.hpval_label,0,1,1,1)

		self.ap_label = QtWidgets.QLabel("AP:")
		self.stat_group.addWidget(self.ap_label,1,0,1,1)
		self.apval_label = QtWidgets.QLabel(str(self.char.get_ap()))
		self.stat_group.addWidget(self.apval_label,1,1,1,1)

		self.mp_label = QtWidgets.QLabel("MP:")
		self.stat_group.addWidget(self.mp_label,2,0,1,1)
		self.mpval_label = QtWidgets.QLabel(str(self.char.get_mp()))
		self.stat_group.addWidget(self.mpval_label,2,1,1,1)

		self.init_label = QtWidgets.QLabel("Init:")
		self.stat_group.addWidget(self.init_label,3,0,1,1)
		self.initval_label = QtWidgets.QLabel(str(self.char.get_initiative()))
		self.stat_group.addWidget(self.initval_label,3,1,1,1)


		self.hp_up = QtWidgets.QPushButton("+")
		tip = """Add points to HP
cost: 1"""
		self.hp_up.setToolTip(tip)
		self.hp_up.clicked.connect(self.increase_hp)
		self.stat_group.addWidget(self.hp_up, 0, 2, 1, 1)

		self.ap_up = QtWidgets.QPushButton("+")
		tip = """Add points to AP
cost: 10"""
		self.ap_up.setToolTip(tip)
		self.ap_up.clicked.connect(self.increase_ap)
		self.stat_group.addWidget(self.ap_up, 1, 2, 1, 1)

		self.mp_up = QtWidgets.QPushButton("+")
		tip = """Add points to MP
cost: 10"""
		self.mp_up.setToolTip(tip)
		self.mp_up.clicked.connect(self.increase_mp)
		self.stat_group.addWidget(self.mp_up, 2, 2, 1, 1)

		self.init_up = QtWidgets.QPushButton("+")
		tip = """Add points to initiative
cost: 1"""
		self.init_up.setToolTip(tip)
		self.init_up.clicked.connect(self.increase_init)
		self.stat_group.addWidget(self.init_up, 3, 2, 1, 1)


		self.str_label = QtWidgets.QLabel("Strength:")
		self.stat_group.addWidget(self.str_label,0,4,1,1)
		self.strval_label = QtWidgets.QLabel(str(self.char.get_strength()))
		self.stat_group.addWidget(self.strval_label,0,5,1,1)

		self.dex_label = QtWidgets.QLabel("Dexterity:")
		self.stat_group.addWidget(self.dex_label,1,4,1,1)
		self.dexval_label = QtWidgets.QLabel(str(self.char.get_dexterity()))
		self.stat_group.addWidget(self.dexval_label,1,5,1,1)

		self.agi_label = QtWidgets.QLabel("Agility:")
		self.stat_group.addWidget(self.agi_label,2,4,1,1)
		self.agival_label = QtWidgets.QLabel(str(self.char.get_agility()))
		self.stat_group.addWidget(self.agival_label,2,5,1,1)


		self.str_up = QtWidgets.QPushButton("+")
		tip = """Add points to STR
cost: 1"""
		self.str_up.setToolTip(tip)
		self.str_up.clicked.connect(self.increase_strength)
		self.stat_group.addWidget(self.str_up, 0, 6, 1, 1)

		self.dex_up = QtWidgets.QPushButton("+")
		tip = """Add points to DEX
cost: 1"""
		self.dex_up.setToolTip(tip)
		self.dex_up.clicked.connect(self.increase_dexterity)
		self.stat_group.addWidget(self.dex_up, 1, 6, 1, 1)

		self.agi_up = QtWidgets.QPushButton("+")
		tip = """Add points to AGI
cost: 1"""
		self.agi_up.setToolTip(tip)
		self.agi_up.clicked.connect(self.increase_agility)
		self.stat_group.addWidget(self.agi_up, 2, 6, 1, 1)

		self.label_box = QtWidgets.QGroupBox()
		self.label_box.setLayout(self.stat_group)
		self.layout.addWidget(self.label_box, 1,0,1,1)


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

			y += 1
			if y >= 4:
				y = 0
				x += 1

		self.group_box = QtWidgets.QGroupBox()
		self.group_box.setLayout(self.button_group)
		self.layout.addWidget(self.group_box, 0,1,2,1)

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
		self.update_signal.emit()

	def increase_dexterity(self):
		self.char.increase_dexterity()
		self.dexval_label.setText(str(self.char.get_dexterity()))
		self.stat_val_label.setText(str(self.char.get_stat_points()))
		self.update_signal.emit()

	def increase_agility(self):
		self.char.increase_agility()
		self.agival_label.setText(str(self.char.get_agility()))
		self.stat_val_label.setText(str(self.char.get_stat_points()))
		self.update_signal.emit()

	def increase_hp(self):
		self.char.increase_agility()
		self.agival_label.setText(str(self.char.get_agility()))
		self.stat_val_label.setText(str(self.char.get_stat_points()))
		self.update_signal.emit()

	def increase_ap(self):
		self.char.increase_agility()
		self.agival_label.setText(str(self.char.get_agility()))
		self.stat_val_label.setText(str(self.char.get_stat_points()))
		self.update_signal.emit()

	def increase_mp(self):
		self.char.increase_agility()
		self.agival_label.setText(str(self.char.get_agility()))
		self.stat_val_label.setText(str(self.char.get_stat_points()))
		self.update_signal.emit()

	def increase_init(self):
		self.char.increase_agility()
		self.agival_label.setText(str(self.char.get_agility()))
		self.stat_val_label.setText(str(self.char.get_stat_points()))
		self.update_signal.emit()

	def unlock_attack(self, key):
		if self.char.get_spell_points() > 0:
			self.char.set_spell_points(self.char.get_spell_points()-1)
			self.char.add_attack(self.attacks[key])
			self.spell_val_label.setText(str(self.char.get_spell_points()))
			self.init_attack_buttons()
