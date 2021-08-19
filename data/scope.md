<link rel="stylesheet" type="text/css" href="mdmobile.css">

# mrl-scope

## business case

* to develop and release a video game on the steam platform
	* professional look and feel

## constraints

* capable of being completed by 1-3 people, within 2 years
* very low budget
* no artist/graphic designer. options:
	1. keep it visually abstract and use rogue-like symbols
	2. diy: rimworld style top down 2d art
	3. build game then find artist later.. use placeholders in the meantime
	4. find an affordable asset package online and build the game to suit the artwork

## features

* 2d: without dedicated gfx artist or programmer this is a necessary constraint as gfx is not a priority
* single player: online multiplayer deemed out of scope
* character based - player controls multiple characters - rpg style
* open world - procedurally generated - focus on simulation
* real time, or turn based
	* currently the game is turn based
	* for a simulation it is preferential that the game is real time

## implementation

### devs

* daniel: wants to focus on game mechanics, AI, simulation
* lex: wants to be an allrounder

### game engine

* godot: feature rich game engine
	* ideal for adding polish to the game: music, graphics, animation etc
	* possibly not such a great simulator: ie - economic system, AI behavior etc

### custom code base + libraries

* python: slow, pleasant to code in, tight integration
	* tcod - has useful pathfinding and field of view alogorithms
	* wasabi2d - barebones but acceptable graphical capabilities
	* pyglet - more sophisticated graphics/games library
* c++: fast, but has pointers, memory management required, somewhat painful intergration
	* SDL2: industry standard library with everything needed for a 2d game
	* SFML: swiss army knife 2d games library 
* rust: fast, safe, but not OO - learning curve to use ECS
	* bracket-lib - excellent set of rogue-like tools
	* tetra - 2d game engine library