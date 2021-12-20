#!/usr/bin/env python3
#-------------------------------------
# imports
import time
import numpy

import tcod

import utils
import char.chargen as chargen
import procgen
import tile
import gui.ui as ui
from gui.message import MessageLog

#-------------------------------------
# variables

# ts = tcod.tileset.load_tilesheet("images/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
ts = tcod.tileset.load_truetype_font("images/ubuntumono-r.ttf", 16, 16) 

messages = MessageLog()
game_map = procgen.create_map(utils.map_ui.w, utils.map_ui.h)

#-------------------------------------
def render(context: tcod.context, console: tcod.Console):
    console.tiles_rgb[0:game_map.width, 0:game_map.height] = \
        numpy.select(condlist=[game_map.visible, game_map.explored], \
            choicelist=[game_map.tiles["light"], game_map.tiles["dark"]], \
                default=tile.SHROUD )

    for i, pc in enumerate(chargen.pcList.clist):
        if i == chargen.pcList.hilited:
            console.print(x=pc.dest_x, y=pc.dest_y, string='*', fg=pc.color)
            console.print(x=pc.x, y=pc.y, string=pc.faction, fg=pc.color, bg=utils.lime)
        else:
            console.print(x=pc.x, y=pc.y, string=pc.faction, fg=pc.color)

    for npc in chargen.npcList:
        if game_map.visible[npc.x, npc.y]:
            console.print(x=npc.x, y=npc.y, string=npc.faction, fg=npc.color)

    messages.render\
        (console, x=utils.mess_ui.x, y=utils.mess_ui.y, w=utils.mess_ui.w, h=utils.mess_ui.h)

    ui.render_CharInfo(console)
    ui.set_gameLabels(console)

    context.present(console) # update the screen
    console.clear()

#-------------------------------------
def handle_events(context: tcod.context):
    for event in tcod.event.get(): 
        if event.type == "KEYDOWN":
            if event.sym == tcod.event.K_SPACE:
                if utils.paused is False:
                    utils.paused = True
                else:
                    utils.paused = False

        if event.type == "MOUSEBUTTONUP":
            if event.button == tcod.event.BUTTON_LEFT:
                context.convert_event(event)

                if game_map.in_bounds(event.tile.x, event.tile.y):
                    for i, pc in enumerate(chargen.pcList.clist):
                        if pc.x == event.tile.x and pc.y == event.tile.y:
                            chargen.pcList.hilited = i

            if event.button == tcod.event.BUTTON_RIGHT:
                context.convert_event(event)

                if game_map.in_bounds(event.tile.x, event.tile.y):
                    chargen.pcList.clist[chargen.pcList.hilited]\
                        .set_dest(event.tile.x, event.tile.y)

        if event.type == "MOUSEMOTION":
            context.convert_event(event)
            ui.select_entity(event.tile.x, event.tile.y, game_map)

        if event.type == "QUIT":
            raise SystemExit()

#-------------------------------------
def update_game(context: tcod.context, root_console: tcod.Console):
    for pc in chargen.pcList.clist:
        if pc.dest is True:
            pc.move(game_map)
        render(context, root_console)
 
    # for npc in chargen.npcList:
        # npc.perform_action(game_map, messages)
        # render(context, root_console)

#-------------------------------------
def update_fov():
    game_map.visible[:] = False # reset visible tile game_map array

    for pc in chargen.pcList.clist:
        pc.visible[:] = tcod.map.compute_fov\
            (game_map.tiles["transparent"], (pc.x, pc.y), radius=pc.perception)

        game_map.visible |= pc.visible

    game_map.explored |= game_map.visible # If tile is visible add to explored

#-------------------------------------            
def main() -> None:
	# create the screen
    with tcod.context.new_terminal\
        (utils.screen.w, utils.screen.h, tileset=ts, title="mrl", vsync=True) as context:

    	# creates the console - order affects order of xy variables in numpy
        root_console = tcod.Console(utils.screen.w, utils.screen.h, order="F")

        messages.add_message("welcome to merp rogue-like (mrl)", utils.welcome_text)

        while True: # game loop
            utils.start_time = time.perf_counter()

            handle_events(context)

            if utils.paused is False:
                update_game(context, root_console)

            update_fov() 
            render(context, root_console)

            utils.end_time = time.perf_counter()
            utils.delta_time = 1 // (utils.end_time - utils.start_time)

#-------------------------------------
if __name__ == "__main__":
    main()
