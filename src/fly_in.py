from parsing import ValidateData


def main() -> None:
    try:
        from pydantic import ValidationError
    except ModuleNotFoundError:
        print("Import error: pydantic is not installed, run the "
              "'make install' command first")
        return

    from drone_map import DroneMap

    try:
        file_content: ValidateData = ValidateData(
            "maps/challenger/01_the_impossible_dream.txt")
        parsed_data = file_content.parse_file_content()

        drone_map = DroneMap(**parsed_data)
        drone_map.create_drones()

    except ValidationError as e:
        print(e.errors()[0]['msg'].replace("Value error, ", ""))

    drone_map.update_all_solution()
    drones_solutions = [drone.solution for drone in drone_map.drones]

    try:
        from visual_simulation import VisualSimulation

        simulation = VisualSimulation(drones_solutions, drone_map)
        simulation.run()
    except ModuleNotFoundError:
        print("Import error: pygame is not installed, run the "
              "'make install' command first")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
