from __future__ import annotations
from dijkstra import Dijkstra
from pydantic import BaseModel, Field
from typing import Annotated
from hub import Hub


Coordinate = Annotated[int, Field(ge=0, le=200)]


class Drone(BaseModel):

    id: int = Field(ge=1, le=100)
    solution: list[Hub] = Field(default_factory=list)
    position: list[Coordinate, Coordinate] = Field(default_factory=list)

    def get_path_solution(self) -> None:
        """
        Call the Dijkstra algrithm to find the shortest path
        between the entry and the exit.
        """
        self.solution = Dijkstra.find_shortest_path(self.id)

    def simulate_turn(self, turn: int) -> None:
        """
        Simulate a turn.
        Print the turn output of the drone (current position with ID)
        """
        if not self.solution:
            return
        if turn > len(self.solution) or turn < 0:
            return

        self.update_position(turn)
        self.print_current_position_and_id(turn)

    def simulate_reverse_turn(self, turn: int) -> None:
        """
        Go back one turn into the simulation.
        Print the turn output of the drone (current position with ID)
        """
        if not self.solution:
            return
        if turn > len(self.solution) or turn < 0:
            return

        self.update_position(turn)
        self.print_current_position_and_id(turn)

    def print_current_position_and_id(self, turn: int) -> None:
        """Print the turn output of the drone (current position with ID)"""
        print(f"D{self.id}-{self.solution[turn].name} ", end="")

    def update_position(self, turn: int) -> None:
        self.position.clear()
        self.position.append(self.solution[turn].coordinates[0])
        self.position.append(self.solution[turn].coordinates[1])

    @staticmethod
    def drone_factory(nb_of_drone: int, starting_hub: Hub) -> list[Drone]:
        """Create all the drone at once."""
        created_drones: list[Drone] = []

        for i in range(nb_of_drone):
            new_drone = Drone(id=i + 1,
                              solution=[],
                              position=[])
            created_drones.append(new_drone)
        return created_drones


def main() -> None:
    try:
        drone = Drone(id=1,
                      solution=[Hub(
                        name="hub1",
                        coordinates=['4', '1'],
                        zone="normal",
                        color="red",
                        max_drones=50,
                        neighbors=[],
                        ), Hub(
                        name="hub2",
                        coordinates=['3', '5'],
                        zone="normal",
                        color="red",
                        max_drones=50,
                        neighbors=[]),
                        ],
                      position=[1, 0])
        drone.simulate_turn(turn=0)
        print(drone.position)
        drone.simulate_turn(turn=1)
        print(drone.position)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
