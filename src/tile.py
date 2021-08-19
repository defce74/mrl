#!/usr/bin/env python3
#-------------------------------------
from typing import List, Tuple

import numpy

import tcod

import utils
import char.chargen as chargen

#-------------------------------------
# Tile graphics struct type compatible with Console.tiles_rgb.
#	- int32: unicode codepoint
#	- 3B: 3 unsigned bytes for RGB colors
graphic_dt = numpy.dtype([ ("ch", numpy.int32), ("fg", "3B"), ("bg", "3B"), ])

# Tile struct used for statically defined tile data.
#	- walkable: True if this tile can be walked over.
#	- transparent: True if this tile doesn't block FOV
#	- dark: Graphics for when this tile is not in FOV
tile_dt = numpy.dtype([ ("walkable", numpy.bool), ("transparent", numpy.bool), \
	("dark", graphic_dt), ("light", graphic_dt) ])

#-------------------------------------
# helper function to declare numpy dtype ndarray data types
#	- *: enforces the use of keywords
def new_tile(*, walkable: int, transparent: int, dark: graphic_dt, light: graphic_dt ) \
	-> numpy.ndarray:
    return numpy.array((walkable, transparent, dark, light), dtype=tile_dt)

# fog of war
SHROUD = numpy.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

# tile types
floor = new_tile( walkable=True, transparent=True, \
	dark=(ord(" "), (utils.maroon), (50, 50, 150)), light=(ord(" "), (utils.maroon), (200, 180, 50)) )
wall = new_tile( walkable=False, transparent=False, \
	dark=(ord(" "), (utils.blue), (0, 0, 100)), light=(ord(" "), (utils.maroon), (130, 110, 50)) )

#-------------------------------------
class Map():
	def __init__(self, width: int, height: int):
		self.width = width
		self.height = height

		# numpy.full: create a 2d array filled with the same values
		self.tiles = numpy.full((self.width, self.height), fill_value = wall, order="F")
		self.visible = numpy.full((self.width, self.height), fill_value=False, order="F")
		self.explored = numpy.full((self.width, self.height), fill_value=False, order="F")

	#-------------------------------------
	# return True if x and y are inside of the bounds of this map
	def in_bounds(self, x: int, y: int) -> bool:
		return 0 <= x < self.width and 0 <= y < self.height

	#-------------------------------------
	# Compute and return a path to the dest position
	#	- If there is no valid path then return an empty list
	# 	- cost: low number causes characters to crowd, 
	# 		- high number causes characters to take a detour.
	def get_path_to(self, x, y, dest_x, dest_y) -> List[Tuple[int, int]]:
		cost = numpy.array(self.tiles["walkable"], dtype=numpy.int8) # copy walkable array from gamemap

		for npc in chargen.npcList:
			if cost[npc.x, npc.y]: # check for blocking npcs
				cost[npc.x, npc.y] += 10 

		for pc in chargen.pcList.clist:
			if cost[pc.x, pc.y]: # check for blocking pcs
				cost[pc.x, pc.y] += 10 

        # Create a graph from the cost array and pass that graph to a new pathfinder.
		graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=0)
		pathfinder = tcod.path.Pathfinder(graph)
		pathfinder.add_root((x, y)) # Start position.

        # Compute the path to the destination and remove the starting point.
		path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

		return [(i[0], i[1]) for i in path] # Convert List[List[int]] to List[Tuple[int, int]]
