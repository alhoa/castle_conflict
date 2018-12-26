from PyQt5 import QtWidgets, QtCore, QtGui
from exceptions import *

import random

#This class handles all graphical elements of the game

class ResultWindow(QtWidgets.QMainWindow):

	def __init__(self, game):
		super().__init__()
		
		self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
		self.layout = QtWidgets.QGridLayout() #Use grid layout
		self.centralWidget().setLayout(self.layout)

		self.game = game

		self.setGeometry(0, 0, 720, 360) #window size
		#Initialize graphical elements
		self.init_labels()
		self.init_buttons()


		self.show()


	def init_labels(self):

		self.label_group = QtWidgets.QGridLayout()

		index = 0

		for player in self.game.get_players():

			nameval_label = QtWidgets.QLabel(player.get_name())
			self.label_group.addWidget(nameval_label, index+1, 0,1,1)

			level_label = QtWidgets.QLabel("Level:")
			self.label_group.addWidget(level_label, index+1,1,1,1)

			level_val_label = QtWidgets.QLabel(str(player.get_level()))
			self.label_group.addWidget(level_val_label,index+1,2,1,1)

			hp_label = QtWidgets.QLabel("Xp gained:")
			self.label_group.addWidget(hp_label,index,3,1,1)

			hpval_label = QtWidgets.QLabel(str(player.get_xp()))
			self.label_group.addWidget(hpval_label,index,4,1,1)

			normal_style = """
			QProgressBar{{
				border: 1px solid grey;
				border-radius: 3px;
				text-align: center
			}}

			QProgressBar::chunk {{
				background: qlineargradient(x1: 0, x2: 1 ,stop: 0 gray, stop: {} gray, stop: {} #05B8CC stop: 1.0 #05B8CC);
			}}
			"""

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

			max_xp = player.get_xp_for_next_lvl() #Value for next level


			progress_bar = QtWidgets.QProgressBar()

			if player.get_xp() == 0:
				progress_bar.setStyleSheet(no_xp_style)
			else:
				if (player.get_xp()+player.get_stored_xp()) == 0:
					percent_new = 0
				else:
					percent_new = player.get_stored_xp()/(player.get_xp()+player.get_stored_xp())
				progress_bar.setStyleSheet(normal_style.format(percent_new, percent_new+0.0001)) 

			progress_bar.setRange(0,max_xp)
			
			progress_bar.setValue(player.get_xp()+player.get_stored_xp())
			self.label_group.addWidget(progress_bar,index+1,3,1,4)

			ap_label = QtWidgets.QLabel("Total xp:")
			self.label_group.addWidget(ap_label,index,5,1,1)

			apval_label = QtWidgets.QLabel(str(player.get_xp()+player.get_stored_xp()))
			self.label_group.addWidget(apval_label,index,6,1,1)

			mp_label = QtWidgets.QLabel("Loot:")
			self.label_group.addWidget(mp_label,index+1,7,1,1)

			mpval_label = QtWidgets.QLabel(str(player.get_hp()))
			self.label_group.addWidget(mpval_label,index+1,8,1,1)

			index += 2

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
