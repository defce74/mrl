#!/usr/bin/env python3
#-------------------------------------
# imports
import numpy
import tcod
import utils
import char.character as character
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
def render(context: tcod.context, console: tcod.Console, hilited: character.Character):
    console.tiles_rgb[0:game_map.width, 0:game_map.height] = \
        numpy.select(condlist=[game_map.visible, game_map.explored], \
            choicelist=[game_map.tiles["light"], game_map.tiles["dark"]], \
                default=tile.SHROUD )

    for pc in game_map.pcs:
        if pc is hilited:
            console.print(x=pc.x, y=pc.y, string=pc.faction, fg=pc.color, bg=utils.lime)
        else:
            console.print(x=pc.x, y=pc.y, string=pc.faction, fg=pc.color)

    for npc in game_map.npcs:
        if game_map.visible[npc.x, npc.y]:
            if npc is hilited:
                console.print\
                    (x=npc.x, y=npc.y, string=npc.faction, fg=npc.color, bg=utils.lime)
            else:
                console.print(x=npc.x, y=npc.y, string=npc.faction, fg=npc.color)

    messages.render\
        (console, x=utils.mess_ui.x, y=utils.mess_ui.y, w=utils.mess_ui.w, h=utils.mess_ui.h)
    ui.render_info(console)

    context.present(console) # update the screen
    console.clear()

#-------------------------------------
def handle_events(context: tcod.context, pc: character.Character):
    for event in tcod.event.wait(): # capture user input 
        if event.type == "KEYDOWN":
            if event.sym == tcod.event.K_UP:
                pc.move(0, -1, game_map, messages)
                utils.gameState = 2 # new turn
            if event.sym == tcod.event.K_DOWN:
                pc.move(0, 1, game_map, messages)
                utils.gameState = 2 # new turn
            if event.sym == tcod.event.K_LEFT:
                pc.move(-1, 0, game_map, messages)
                utils.gameState = 2 # new turn
            if event.sym == tcod.event.K_RIGHT:
                pc.move(1, 0, game_map, messages)
                utils.gameState = 2 # new turn

        if event.type == "MOUSEMOTION":
            context.convert_event(event)
            ui.select_entity(event.tile.x, event.tile.y, game_map)

        if event.type == "QUIT":
            raise SystemExit()

#-------------------------------------
def update_game(context: tcod.context, console: tcod.Console):
    for npc in game_map.npcs:
        render(context, console, npc)
        npc.perform_action(game_map, messages)
        pause_game(context, console, npc)

#-------------------------------------
def update_fov():
    game_map.visible[:] = False # reset visible tile game_map array

    for pc in game_map.pcs:
        pc.visible[:] = tcod.map.compute_fov\
            (game_map.tiles["transparent"], (pc.x, pc.y), radius=pc.perception)

        game_map.visible |= pc.visible

    game_map.explored |= game_map.visible # If tile is visible add to explored

#-------------------------------------
def pause_game(context: tcod.context, console: tcod.Console, c: character.Character):
    paused = True

    while paused:
        for event in tcod.event.wait(): # capture user input 
            if event.type == "KEYDOWN":            
                if event.sym == tcod.event.K_c: # 'c' for continue
                    paused = False

            if event.type == "QUIT":
                raise SystemExit()

            if event.type == "MOUSEMOTION":
                context.convert_event(event)
                ui.select_entity(event.tile.x, event.tile.y, game_map)
                render(context, console, c)

#-------------------------------------            
def main() -> None:
	# create the screen
    with tcod.context.new_terminal\
        (utils.screen.w, utils.screen.h, tileset=ts, title="mrl", vsync=True) as context:
    	# creates the console - order affects order of xy variables in numpy
        root_console = tcod.Console(utils.screen.w, utils.screen.h, order="F")

        messages.add_message("welcome to merp rogue-like (mrl)", utils.welcome_text)

        while True: # game loop
            for pc in game_map.pcs:
                utils.gameState = 1

                while utils.gameState == 1:
                    handle_events(context, pc)
                    update_fov()
                    render(context, root_console, pc)

            update_game(context, root_console)

#-------------------------------------
if __name__ == "__main__":
    main()
