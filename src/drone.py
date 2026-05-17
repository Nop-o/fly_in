from __future__ import annotations
from djikstra import Djikstra


class Drone:
    def __init__(self, id: int) -> None:
        self.id = id
        self.position = 0

    def get_path_solution(self) -> None:
        self.solution = Djikstra.find_shortest_path(self.id).reverse()

    def simulate_turn(self) -> None:
        if not self.solution:
            return
        if len(self.solution) <= self.position:
            return

        self.position += 1
        print(f"D {self.id}-{self.solution[self.position]} ", end="")

    def simulate_reverse_turn(self) -> None:
        if not self.solution:
            return
        if 0 <= self.position:
            return

        self.position -= 1
        print(f"D {self.id}-{self.solution[self.position]} ", end="")

    @staticmethod
    def drone_factory(nb_of_drone: int) -> list[Drone]:
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
