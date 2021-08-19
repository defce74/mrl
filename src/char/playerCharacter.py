# #!/usr/bin/env python3
#-------------------------------------
from char.character import Character

#-------------------------------------
class PlayerCharacter(Character):
	pass

#-------------------------------------
class PlayerCharacter_list():
	def __init__(self, hilited):
		self.clist = [] # list
		self.hilited = hilited
