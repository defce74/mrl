# #!/usr/bin/env python3
#-------------------------------------
from typing import List, Tuple
import textwrap

import tcod

import utils

#-------------------------------------
class Message: 
	def __init__(self, text: str, fg: Tuple[int, int, int]):
		self.text = text
		self.fg = fg

#-------------------------------------
# a list of messages recieved
class MessageLog:
	def __init__(self) -> None:
		self.messages: List[Message] = []

	#-------------------------------------
	# Add a message to this log
	def add_message(self, text: str, fg: Tuple[int, int, int] = utils.white) -> None:
		text = str(len(self.messages)) + ": " + text
		self.messages.append(Message(text, fg))

	#-------------------------------------
	# Render this log over the given area.
	# 	- x, y, w, h: the rectangular region to render onto the console
	# 	- messages are rendered starting at the last message and working backwards
	def render(self, console: tcod.Console, x: int, y: int, w: int, h: int) -> None:
		y_offset = h - 1

		for message in reversed(self.messages):
			for line in reversed(textwrap.wrap(message.text, w)):
				console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
				y_offset -= 1

				if y_offset < 0:
					return  # No more space to print messages.
