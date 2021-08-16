#!/usr/bin/env python3
#-------------------------------------
from __future__ import annotations # allow class to accept an instance of itself as a parameter
from typing import Tuple, Iterator, List
import random
import tcod
import tile
import char.chargen as chargen
#-------------------------------------
class Room:
	def __init__(self, x: int, y: int, width: int, height: int):
		self.x1 = x
		self.y1 = y
		self.x2 = x + width
		self.y2 = y + height

	#-------------------------------------
	@property
	def center(self) -> Tuple[int, int]:
		center_x = int((self.x1 + self.x2) / 2)
		center_y = int((self.y1 + self.y2) / 2)
		return center_x, center_y

	#-------------------------------------
	# Return the inner area of this room as a 2D array index
	# 	- prevents rooms being generated next to each other
	@property
	def inner(self) -> Tuple[slice, slice]:
		return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

	#-------------------------------------
	# Return True if this room overlaps with another Room
	def intersects(self, other: Room) -> bool:
		return self.x1 <= other.x2 and self.x2 >= other.x1 and \
			self.y1 <= other.y2 and self.y2 >= other.y1 

#-------------------------------------
def spawn_character(character, room: Room, dungeon: tile.Map) -> None:
	spawned = False

	while not spawned:
		x = random.randint(room.x1 + 1, room.x2 - 1)
		y = random.randint(room.y1 + 1, room.y2 - 1)

		if not any(npc.x == x and npc.y == y for npc in dungeon.npcs):
			if not any(pc.x == x and pc.y == y for pc in dungeon.pcs):
				character.spawn(x, y)
				spawned = True

#-------------------------------------
# Return an L-shaped tunnel between these two points
def tunnel_between(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:  # 50% chance.
        corner_x, corner_y = x2, y1  # Move horizontally, then vertically.
    else:
        corner_x, corner_y = x1, y2 # Move vertically, then horizontally.

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y # yield: return the values but keep the local state
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

#-------------------------------------
# Generate a new dungeon map
def create_map(width: int, height: int) -> tile.Map:
	dungeon = tile.Map(width, height)
	dungeon.npcs = chargen.npcList
	dungeon.pcs = chargen.pcList

	room_max_size = 18
	room_min_size = 6
	max_rooms = 60

	rooms: List[Room] = []

	for _r in range(max_rooms):
		room_width = random.randint(room_min_size, room_max_size)
		room_height = random.randint(room_min_size, room_max_size)

		x = random.randint(0, dungeon.width - room_width - 1)
		y = random.randint(0, dungeon.height - room_height - 1)
		new_room = Room(x, y, room_width, room_height)

		# Run through the other rooms and see if they intersect with this one.
		if any(new_room.intersects(other_room) for other_room in rooms):
			continue  # This room intersects, so go to the next attempt.

		dungeon.tiles[new_room.inner] = tile.floor # Dig out this rooms inner area.

		if len(rooms) > 0: 
			for x, y in tunnel_between(rooms[-1].center, new_room.center):
				dungeon.tiles[x, y] = tile.floor

		rooms.append(new_room) # append the new room to the list
	
	for c in dungeon.npcs:
		if c.x==0 or c.y==0: 
			r = random.randrange(0, len(rooms))
			spawn_character(c, rooms[r], dungeon)

	for c in dungeon.pcs:
		if c.x==0 or c.y==0: 
			r = random.randrange(0, len(rooms))
			spawn_character(c, rooms[r], dungeon)

	return dungeon
