from __future__ import annotations


class Drone:
    def __init__(self, id: int) -> None:
        self.id = id

    def get_path_solution(self) -> None:
        self.solution = Djikstra.find_shortest_path(self.id).reverse()

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
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
