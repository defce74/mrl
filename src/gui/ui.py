#!/usr/bin/env python3
#-------------------------------------
import tcod

import tile
import char.chargen as chargen
from char.character import Character

#-------------------------------------
class label:
	def __init__(self, x: int=80, y: int=0, text: str=None):
		self.x = x
		self.y = y
		self.text = text

#-------------------------------------
name = label()
faction = label(y=1)
attack = label(y=2)
defence = label(y=3)
health = label(y=4)
perception = label(y=5)
movement = label(y=6)

#-------------------------------------
def select_entity(x: int, y: int, game_map: tile.Map) -> None:
	if game_map.in_bounds(x, y) and game_map.visible[x, y]:
		for pc in chargen.pcList.clist:
			if pc.x == x and pc.y == y:
				set_labels(pc)
		for npc in chargen.npcList:
			if npc.x == x and npc.y == y:
				set_labels(npc)

#-------------------------------------
def render_info(console: tcod.console) -> None:
	# if name.text is not '': 
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
def set_labels(c: Character):
	name.text = c.name
	faction.text = c.faction
	attack.text = str(c.attack)
	defence.text = str(c.defence)
	health.text = str(c.health)
	perception.text = str(c.perception)
	movement.text = str(c.movement)
