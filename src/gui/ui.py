#!/usr/bin/env python3
#-------------------------------------
import tcod

import utils
import tile
import char.chargen as chargen
from char.character import Character

#-------------------------------------
class label:
	def __init__(self, x: int=0, y: int=0, text: str=None):
		self.x = x
		self.y = y
		self.text = text

#-------------------------------------
# character ui labels
name = label(x=utils.char_ui.x)
faction = label(x=utils.char_ui.x, y=1)
attack = label(x=utils.char_ui.x, y=2)
defence = label(x=utils.char_ui.x, y=3)
health = label(x=utils.char_ui.x, y=4)
perception = label(x=utils.char_ui.x, y=5)
movement = label(x=utils.char_ui.x, y=6)

#-------------------------------------
def select_entity(x: int, y: int, game_map: tile.Map) -> None:
	if game_map.in_bounds(x, y) and game_map.visible[x, y]:
		for pc in chargen.pcList.clist:
			if pc.x == x and pc.y == y:
				set_charLabels(pc)
		for npc in chargen.npcList:
			if npc.x == x and npc.y == y:
				set_charLabels(npc)

#-------------------------------------
def render_CharInfo(console: tcod.console) -> None:
	if name.text: 
		console.print(x=name.x, y=name.y, string='name: ', alignment=tcod.LEFT)
		console.print(x=faction.x, y=faction.y, string='faction: ', alignment=tcod.LEFT)
		console.print(x=attack.x, y=attack.y, string='attack: ', alignment=tcod.LEFT)
		console.print(x=defence.x, y=defence.y, string='defence: ', alignment=tcod.LEFT)
		console.print(x=health.x, y=health.y, string='health: ', alignment=tcod.LEFT)
		console.print(x=perception.x, y=perception.y, string='perception: ', alignment=tcod.LEFT)
		console.print(x=movement.x, y=movement.y, string='movement: ', alignment=tcod.LEFT)

		console.print(x=name.x+15, y=name.y, string=name.text, alignment=tcod.RIGHT)
		console.print(x=faction.x+15, y=faction.y, string=faction.text, alignment=tcod.RIGHT)
		console.print(x=attack.x+15, y=attack.y, string=attack.text, alignment=tcod.RIGHT)
		console.print(x=defence.x+15, y=defence.y, string=defence.text, alignment=tcod.RIGHT)
		console.print(x=health.x+15, y=health.y, string=health.text, alignment=tcod.RIGHT)
		console.print(x=perception.x+15, y=perception.y, string=perception.text, alignment=tcod.RIGHT)
		console.print(x=movement.x+15, y=movement.y, string=movement.text, alignment=tcod.RIGHT)

#-------------------------------------
def set_charLabels(c: Character):
	name.text = c.name
	faction.text = c.faction
	attack.text = str(c.attack)
	defence.text = str(c.defence)
	health.text = str(c.health)
	perception.text = str(c.perception)
	movement.text = str(c.movement)

#-------------------------------------
# game ui labels
delta = label(x=utils.game_ui.x, y=utils.game_ui.y)
paused_label = label(x=utils.game_ui.x, y=utils.game_ui.y+1)

#-------------------------------------
def set_gameLabels(console: tcod.console):
	delta.text = str(utils.delta_time)
	console.print(x=delta.x, y=delta.y, string=delta.text, alignment=tcod.LEFT, fg=utils.lime)

	paused_label.text = str(utils.paused)
	console.print(x=paused_label.x, y=paused_label.y, string="paused: " + paused_label.text, \
		alignment=tcod.LEFT, fg=utils.lime)
