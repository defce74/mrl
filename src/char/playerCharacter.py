# #!/usr/bin/env python3
#-------------------------------------
from tile import Map
from char.character import Character
from gui.message import MessageLog
import utils
#-------------------------------------
class PlayerCharacter(Character):
	#-------------------------------------
	def move(self, dx: int, dy: int, gameMap: Map, messages: MessageLog) -> bool:
		collision = False

		if gameMap.tiles["walkable"][self.x + dx, self.y + dy]:

			for npc in gameMap.npcs:
				if npc.x == (self.x + dx) and npc.y == (self.y + dy):
					messages.add_message(f"pc {self.name} attacks {npc.name}", utils.red)
					collision = True

			for pc in gameMap.pcs:
				if pc.x == (self.x + dx) and pc.y == (self.y + dy):
					messages.add_message(f"pc {self.name} greets {pc.name}", utils.blue)
					collision = True

		else: 
			messages.add_message(f"pc {self.name} walks into a wall", utils.grey)
			collision = True

		if not collision:
			self.x += dx
			self.y += dy
			messages.add_message(f"pc {self.name} has moved", utils.brown)

		return collision
