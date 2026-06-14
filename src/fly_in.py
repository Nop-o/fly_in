from .parsing import ValidateData
import sys


def main() -> None:
    try:
        from pydantic import ValidationError
    except ModuleNotFoundError:
        print("Import error: pydantic is not installed, run the "
              "'make install' command first")
        return

    if len(sys.argv) == 1:
        print("Argument error: no arguments provided")
        return
    if len(sys.argv) > 2:
        print("Argument error: too many arguments provided")
        return

    try:
        file_content: ValidateData = ValidateData(sys.argv[1])
        parsed_data = file_content.parse_file_content()

        from .drone_map import DroneMap

        drone_map = DroneMap(**parsed_data)
        drone_map.create_drones()

    except ValidationError as e:
        print(e.errors()[0]['msg'].replace("Value error, ", ""))
        return

    drone_map.update_all_solution()
    drones_solutions = [drone.solution for drone in drone_map.drones]

    try:
        from .visual_simulation import VisualSimulation

        simulation = VisualSimulation(drones_solutions, drone_map)
        simulation.run()
    except ModuleNotFoundError:
        print("Import error: pygame is not installed, run the "
              "'make install' command first")
        return


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
