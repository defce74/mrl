#!/usr/bin/env python3
#-------------------------------------
import sqlite3

from char.playerCharacter import PlayerCharacter
from char.nonPlayerCharacter import NonPlayerCharacter

#--------------------------------------
# characters table: 
#	- r[0]: name
#	- r[1]: faction
#	- r[2]: attack
#	- r[3]: defence
#	- r[4]: health
#	- r[5]: perception
#	- r[6]: movement
def load_characters():
	con = sqlite3.connect('data/pymerp.db')

	for r in con.execute("select * from characters"):
		if r[1] is not '1': # player faction hardcoded to 1
			c = NonPlayerCharacter(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
			npcList.append(c)
		else:
			c = PlayerCharacter(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
			pcList.append(c)

	con.close()

#-------------------------------------
# global variables
pcList = []
npcList = []

load_characters()

#-------------------------------------
