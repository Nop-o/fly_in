*This project has been created as part of the 42 curriculum by [adamez-f](https://github.com/Nop-o).*

# Fly-in

## Table of Contents
- [Fly-in](#fly-in)
	- [Table of Contents](#table-of-contents)

## Description

Autonomous drones are the future of transportation. They are already used in many
industries, such as agriculture, construction, and logistics. They are also used in military
operations, such as surveillance and reconnaissance.
Your task is to design a system that efficiently routes a fleet of drones from a central
base (start) to a target location (end), while navigating this dynamic network under
a set of strict constraints and optimization goals.
You’ll be given a graph representing the network of zones, and a set of constraints
that you must respect.
The graph is represented as a network of connected zones, where connections define possible movement paths between zones.

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
With a given file, I will parse the data and try to recreate a map.

Additionally to the map, a number of drone will be given. The goal will be for each drone to travel from a starting point to an other one, a fast as possible.

## Map components
A drone map has:
- a number of drone
- starting hub
- ending hub
- hubs
- connections

### Hub

Each map has a starting hub and an end hub.

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
For this simulation I used RGB colors (Red Green Blue).
Rgb colors are a set of 3 value between 0 and 255.
For exemple, i reproduced the gold color whith (255, 215, 0).

### 

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
