# #!/usr/bin/env python3
#-------------------------------------
import numpy as np
from utils import map_ui
#-------------------------------------
class Character():
	def __init__(self, name: str, faction: str, attack=0, defence=0, health=0, perception=0, movement=0):
		self.name = name
		self.faction = faction
		self.attack = attack
		self.defence = defence
		self.health = health
		self.perception = perception
		self.movement = movement

		self.x = 0
		self.y = 0
		self.visible = np.full((map_ui.w, map_ui.h), fill_value=False, order="F")
		self.path = []
		self.color = (255, 255, 255)

	#-------------------------------------
	# set character location
	# use location to spawn the character during level gen
	def spawn(self, x: int, y: int):
		self.x = x
		self.y = y
