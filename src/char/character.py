# #!/usr/bin/env python3
#-------------------------------------
import numpy as np

from time import sleep

from utils import map_ui
from tile import Map
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
		self.dest_x = 0
		self.dest_y = 0
		self.visible = np.full((map_ui.w, map_ui.h), fill_value=False, order="F") # fov
		self.path = [] # pathfinding data structure
		self.color = (255, 255, 255)

	#-------------------------------------
	# set character location
	# use location to spawn the character during level gen
	def spawn(self, x: int, y: int):
		self.x = x
		self.y = y

	#-------------------------------------
	# set character destination
	def set_dest(self, x, y, gameMap: Map):
		if self.visible[x, y]: # if selected dest is within fov
			self.dest_x = x
			self.dest_y = y
			self.path = gameMap.get_path_to(self.x, self.y, self.dest_x, self.dest_y)

	#-------------------------------------
	# set character destination
	def move(self):
		if self.path:
			sleep(1/self.movement)
			self.x, self.y = self.path.pop(0) # first step in the path
