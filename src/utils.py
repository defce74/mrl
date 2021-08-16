#!/usr/bin/env python3
#-------------------------------------
from random import randint

#-------------------------------------
class rect:
	def __init__(self, x: int, y: int, w: int, h: int):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

#-------------------------------------
# gameState: 
#	- 1: pc's turn
#	- 2: npc's turn
gameState = int(1)

screen = rect(0, 0, 100, 50)
map_ui = rect(0, 0, 80, 40)
mess_ui = rect(0, 40, 80, 10)
info_ui = rect(80, 0, 20, 50)

#-------------------------------------
# color constants
blue =(38, 139, 205)
lime = (170, 255, 170)
orange = (178, 122, 26)
grey = (150, 150, 148)
brown = (62, 62, 62)
maroon = (99, 49, 54)
green = (0x00, 0x2b, 0x36)
teal = (0x2A, 0xA1, 0x98)
white = (0x93, 0xA1, 0xA1)
red = (0xCB, 0x4B, 0x16)

black = (0x0, 0x0, 0x0)
player_atk = (0xE0, 0xE0, 0xE0)
enemy_atk = (0xFF, 0xC0, 0xC0)
player_die = (0xFF, 0x30, 0x30)
enemy_die = (0xFF, 0xA0, 0x30)
welcome_text = (0x20, 0xA0, 0xFF)

#--------------------------------------
# unmodified percentile dice roll
def um_percentile() -> int:
	return randint(1, 101)
	