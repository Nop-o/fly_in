class Drone:
    def __init__(self, color: str) -> None:
        self.color = color

    @staticmethod
    def drone_factory(nb_of_drone: int, color: str) -> list['Drone']:
        created_drones: list[Drone] = []
        for i in range(nb_of_drone):
            new_drone = Drone(color)
            created_drones.append(new_drone)
        return created_drones


def main() -> None:
    pass


if __name__ == "__main__":
    main()
