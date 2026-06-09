from __future__ import annotations
from dijkstra import Dijkstra
from hub import Hub
from pydantic import BaseModel, Field
from typing import Annotated


Coordinate = Annotated[int, Field(ge=0, le=200)]


class Drone(BaseModel):

    id: int = Field(ge=1, le=100)
    solution: dict[
        int, tuple[str, tuple[int, int]]] = Field(default_factory=dict)
    last_position: str = Field(default_factory=str)

    def get_path_solution(self, hubs: dict[str, Hub], start_hub: Hub,
                          end_hub: Hub) -> None:
        """
        Call the Dijkstra algrithm to find the shortest path
        between the entry and the exit.
        """
        algorithm = Dijkstra(start_hub, end_hub, hubs)
        self.solution = algorithm.find_solution_and_update_hub_capacity()

    def print_current_position_and_id(self, turn: int) -> None:
        """Print the turn output of the drone (current position with ID)"""
        if not self.solution:
            return
        if turn not in self.solution.keys():
            return
        if self.solution[turn][0] == self.last_position:
            return

        print(f"D{self.id}-{self.solution[turn][0]} ", end="")
        self.last_position = self.solution[turn][0]

    @staticmethod
    def drone_factory(nb_of_drone: int) -> list[Drone]:
        """Create all the drone at once."""
        created_drones: list[Drone] = []

        for i in range(nb_of_drone):
            new_drone = Drone(id=i + 1,
                              solution={},)
            created_drones.append(new_drone)
        return created_drones
