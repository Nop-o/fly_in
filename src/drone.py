class Drone:
    def __init__(self, id: int) -> None:
        self.id = id

    @staticmethod
    def drone_factory(nb_of_drone: int) -> list['Drone']:
        created_drones: list[Drone] = []
        for i in range(nb_of_drone):
            new_drone = Drone(i + 1)
            created_drones.append(new_drone)
        return created_drones


def main() -> None:
    pass


if __name__ == "__main__":
    main()
