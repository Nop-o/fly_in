*This project has been created as part of the 42 curriculum by [adamez-f](https://github.com/Nop-o).*

# Fly-in

## Table of Contents
- [Fly-in](#fly-in)
	- [Table of Contents](#table-of-contents)
    - [Description](#description)
    - [Instructions](#instructions)
        - [All available commands](#all-available-commands)
    - [Parsing](#parsing)
    - [Map components](#map-components)
        - [Hub](#hub)
        - [Connection](#connection)
        - [Zone type](#zone-type)
        - [Colors](#colors)
    - [Maps](#maps)
        - [Easy](#easy)
        - [Medium](#medium)
        - [Hard](#hard)
        - [Challenger](#challenger)
    - [Resources](#resources)

## Description

The goal of this porject is to design a system that efficiently routes a fleet of drones from a central
base (start) to a target location (end), while navigating a dynamic network (graph) under
a set of strict constraints and optimization goals.

The graph is represented as a network of connected zones, where connections define possible movement paths between zones.

To find an efficient road for the drones we use the Dijkstra algorithm. Each drone will calculate his shortest path, then he will update each hub/connection capacity per turn. 

## Instructions
To compile the project, use the provided `Makefile`:

### All available commands
| Command | Description |
| :--- | :--- |
| `make install` | Create virtual environment and install dependencies |
| `make clean` | Remove all temporary files and caches |
| `make run` | Execute the main script |
| `make lint` | Run flake8 and mypy with standard checks |
| `make lint-strict` | Run flake8 and mypy with strict mode |
| `make debug` | Run the main script in debug mode (pdb) |
| `make help` | Show an help message |


## Parsing
With a given file, we parse the data and try to recreate a map.

## Map components
A drone map has:
- a number of drone
- starting hub
- ending hub
- hubs
- connections

### Hub

Each map has a starting hub, an end hub and an number N of hubs.

A hub has:
- a name
- coordinates
- zone type*
- a color*
- a max drone capacity
- a list of neighbors: connected hubs + the connection
- a turn capacity: a dynamic list of the number of drone being on the hub at a given turn 

### Connection
Hubs are linked with connections.
A connection has:
- hub_1_name
- hub_2_name
- a max drone capacity
- a turn capacity: a dynamic list of the number of drone being on the connection at a given turn 

#### Zone type

All hubs have a specific zone type.
There are 4 possible types and each takes a specific number of turn to acces:
- NORMAL: 1 turn
- PRIORITY: 1 turn, if possible, you should go to this hub instead of any other one
- BLOCKED: No access, it's a dead end
- RESTRICTED: 2 turns

#### Colors
All hubs have a color.
For this simulation we use RGB colors (Red Green Blue).
Rgb colors are a set of 3 value between 0 and 255.
For exemple, we reproduce the gold color whith (255, 215, 0).


## Maps
With the subject, additional maps where given.
To try them out, go to the fly_in.py file and add one of the map path as an argument to this function : `file_content: ValidateData = ValidateData(<map_path>)`

### Easy
- `maps/easy/01_linear_path.txt`
- `maps/easy/02_simple_fork.txt`
- `maps/easy/03_basic_capacity.txt`
### Medium

- `maps/medium/01_dead_end_trap.txt`
- `maps/medium/02_circular_loop.txt`
- `maps/medium/03_priority_puzzle.txt`

### Hard
- `maps/hard/01_maze_nightmare.txt`
- `maps/hard/02_capacity_hell.txt`
- `maps/hard/03_ultimate_challenge.txt`

### Challenger
- `maps/challenger/01_the_impossible_dream.txt`


## Resources
[codecademy: Dijkstra algorithm](https://www.codecademy.com/article/dijkstras-shortest-path-algorithm)  
[Excalidraw: Visual representation](https://excalidraw.com/)
