# #!/usr/bin/env python3
#-------------------------------------
from __future__ import annotations
from typing import TypeVar, TYPE_CHECKING

import math

import tcod

import utils

import char.chargen as chargen
from gui.message import MessageLog
from char.character import Character

if TYPE_CHECKING:
    from tile import Map

T = TypeVar("T", bound="Character")

#-------------------------------------
class NonPlayerCharacter(Character):
	#-------------------------------------
	def perform_action(self, gameMap: Map, messages: MessageLog):
		shortestDist = 100 # arbitrary high number
		target = None

		self.visible[:] = tcod.map.compute_fov \
            (gameMap.tiles["transparent"], (self.x, self.y), radius=self.perception)

		for pc in chargen.pcList.clist:
			if self.visible[pc.x, pc.y]: # if pc is seen calculate distance
				dx = pow((pc.x - self.x), 2)
				dy = pow((pc.y - self.y), 2)
				dist = math.sqrt(dx + dy) # euclidean distance
				# dist = max(abs(dx), abs(dy)) # Chebyshev distance

				if dist < shortestDist:
					shortestDist = dist
					target = pc # target is closest pc seen

		if target: 
			if shortestDist <= 1: 
				messages.add_message(f"npc {self.name} attacks {target.name}", utils.red)
			else:
				self.path = gameMap.get_path_to(self.x, self.y, target.x, target.y)
				self.move()

				messages.add_message\
					(f"npc {self.name} is moving towards {target.name} {shortestDist:3.2f}", \
						utils.orange)
