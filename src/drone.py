from __future__ import annotations
from djkstra import Dijkstra


class Drone:
    def __init__(self, id: int) -> None:
        self.id = id
        self.position = 0

    def get_path_solution(self) -> None:
        """
        Call the Dijkstra algrithm to find the shortest path 
        between the entry and the exit.
        """
        self.solution = Dijkstra.find_shortest_path(self.id).reverse()

    def simulate_turn(self) -> None:
        """
        Simulate a turn.
        Print the turn output of the drone (current position with ID)
        """
        if not self.solution:
            return
        if len(self.solution) <= self.position:
            return

        self.position += 1
        self.print_current_position_and_id()

    def simulate_reverse_turn(self) -> None:
        """
        Go back one turn into the simulation.
        Print the turn output of the drone (current position with ID)
        """
        if not self.solution:
            return
        if 0 <= self.position:
            return

        self.position -= 1
        self.print_current_position_and_id()

    def print_current_position_and_id(self) -> None:
        """Print the turn output of the drone (current position with ID)"""
        print(f"D {self.id}-{self.solution[self.position]} ", end="")

    @staticmethod
    def drone_factory(nb_of_drone: int) -> list[Drone]:
        """Create all the drone at once."""
        created_drones: list[Drone] = []

        for i in range(nb_of_drone):
            new_drone = Drone(i + 1)
            created_drones.append(new_drone)
        return created_drones


def main() -> None:
    try:
        drone = Drone(id=1)
        print(drone.id)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
