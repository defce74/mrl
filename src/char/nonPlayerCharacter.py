# #!/usr/bin/env python3
#-------------------------------------
from __future__ import annotations
from typing import TypeVar, TYPE_CHECKING, List, Tuple

import math
import numpy as np

import tcod
import utils
from gui.message import MessageLog
from char.character import Character

if TYPE_CHECKING:
    from tile import Map

T = TypeVar("T", bound="Character")

#-------------------------------------
class NonPlayerCharacter(Character):
	#-------------------------------------
	def move(self, dx: int, dy: int, gameMap: Map, messages: MessageLog) -> bool:
		collision = False

		for npc in gameMap.npcs:
			if npc.x == self.x + dx and npc.y == self.y + dy:
				messages.add_message(f"npc {self.name} is blocked by {npc.name}", utils.grey)
				collision = True

		if not collision:
			self.x += dx
			self.y += dy

		return collision

	#-------------------------------------
	def perform_action(self, gameMap: Map, messages: MessageLog):
		shortestDist = 100 # arbitrary high number
		target = None

		self.visible[:] = tcod.map.compute_fov \
            (gameMap.tiles["transparent"], (self.x, self.y), radius=self.perception)

		for pc in gameMap.pcs:
			if self.visible[pc.x, pc.y]:
				dx = pow((pc.x - self.x), 2)
				dy = pow((pc.y - self.y), 2)
				dist = math.sqrt(dx + dy) # euclidean distance
				# dist = max(abs(dx), abs(dy)) # Chebyshev distance

				if dist < shortestDist:
					shortestDist = dist
					target = pc

		if target: 
			if shortestDist <= 1: 
				messages.add_message(f"npc {self.name} attacks {target.name}", utils.red)
			else:
				self.path = self.get_path_to(target.x, target.y, gameMap)

				if self.path:
					dest_x , dest_y = self.path.pop(0) # first step in the path
					collision = self.move(dest_x - self.x, dest_y - self.y, gameMap, messages)

					if not collision: 
						messages.add_message\
							(f"npc {self.name} is moving towards {target.name} {shortestDist:3.2f}", \
								utils.orange)
		else:
			messages.add_message(f"npc {self.name} is waiting", utils.lime)

	#-------------------------------------
	# Compute and return a path to the target position
	#	- If there is no valid path then return an empty list
	# 	- cost: low number enemies will crowd behind each other, 
	# 		- high number enemies will take longer paths to surround the target.
	def get_path_to(self, dest_x: int, dest_y: int, gameMap: Map) -> List[Tuple[int, int]]:
		cost = np.array(gameMap.tiles["walkable"], dtype=np.int8) # copy walkable array from gamemap

		for npc in gameMap.npcs:
			if cost[npc.x, npc.y]: # check for blocking npcs
				cost[npc.x, npc.y] += 10 

        # Create a graph from the cost array and pass that graph to a new pathfinder.
		graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=0)
		pathfinder = tcod.path.Pathfinder(graph)
		pathfinder.add_root((self.x, self.y)) # Start position.

        # Compute the path to the destination and remove the starting point.
		path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

		return [(i[0], i[1]) for i in path] # Convert List[List[int]] to List[Tuple[int, int]]
