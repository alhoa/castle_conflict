# Castle Conflict

Castle Conflict is a small strategy game written in python and PyQt for the CS-A1121 -course.

![Game Title](/src/graphics/title.png)

### 1. Folder structure

All documentation related to the project is found in the /docs folder. The source python scripts are all in the same /src folder. Additionall, the /src folder contains subfolders, which store all of the game assets and saves. Currently (24.12.2018) there is only one exapmle save file in the saves folder. 

### 2. Käyttöohje

The UI mechanics are shown in the documentation found in the docs folder. Unfortunately all of this documentation is currently in finnish. To play the game run the main.py program. The user is presented with an initial splash screen where it is possible to load saves and run them. After succesfully starting a game, the game progresses as follows. 

First the player is presented with a spawning phase where he/she can choose the starting positions for the characters. This is done by clicking on the blue portals on the map. The turn order is the same as the spawning order and it is determined based on the stats of the character and enemies. The white indicator on the turn list shows the active player. Additionally, by clickin on the characters in the turn list, the player can get more information about the clicked character.

After spawning all characters, the game begins. All characters have a limited amount of action points (AP) and movement points (MP), which they can use during their turns. On the righth side of these labels are the buttons for ending the turn or attacking. By default, the characters try to move on the battlefield, which is simply done bly clicking the desired destination. 

After clicking an attack button, the player is shown all possible squares, whcih the attack can hit. If the player wants to find out more information about the attacks, they can hover over the buttons in which case a tool tip is displayed. 

The game ends when all characters from one side have lost all of their hitpoints (HP). In this case, the player is sent back to the initial screen where it is possible to play the next game in the sequence or load a new save file. 


### Saves

The save file is divided into blocks which are formed as follows:

\#<br/>
[BLOCK NAME] : [possible parameter]<br/>
[PARAM 1] : [VALUE 1] : [VALUE 2]<br/>
[PARAM 2] : [VALUE 3]<br/>
/#<br/>

The save file must atleast include an Information block, one game, one player and one enemy. An example save is provided in the /src/saves folder

### Maps

The map files are included in the maps folder. ALl maps must be sved in .bmp for the parser to work.
Additionally, the /src/maps folder includes a maps.txt file, which has all of the relationships between pixel values and objects in the game. The mapping format is as follows:

<br/>
R: G: B: Blocks vision (0/1): Blocks movement (0/1): icon file name<br/>
<br/>
255	: 255	: 255	: 0: 0: NONE<br/>
255	: 0		: 0		: 1: 1: WALL<br/>
0	: 255	: 0		: 0: 0: PLAYER_SPAWN<br/>
<br/>

The colors must have the exact rgb value to be detected and all other colors will be interpreted as ground.

### Enemies

All enemy stats corresponding to their levels are given in the enemy_stats.txt file found in /src/characters. The game will now be able to load enemies with different levels than those defined in this file. The format of the file is: 

\#<br/>
[ENEMY NAME]<br/>
[AI TYPE] :  [LEVEL A] : [LEVEL B] : [LEVEL C]<br/>
[PARAM 1] : [VALUE 1 A] : [VALUE 1 B] : [VALUE 1 C]<br/>
[PARAM 2] : [VALUE 2 A] : [VALUE 2 B] : [VALUE 2 C]<br/>
[PARAM 3] : [VALUE 3 A] : [VALUE 3 B] : [VALUE 3 C]<br/>
/#<br/>



