from parsing import ValidateData
from drone_map import DroneMap
from drone import Drone
from djikstra import Djikstra
from pydantic import ValidationError


def main() -> None:
    try:
        file_content: ValidateData = ValidateData("test.txt")
        parsed_data = file_content.parse_file_content()
        drone_map = DroneMap(**parsed_data)
        drones = Drone.drone_factory(drone_map.nb_drones)
        djikstra_solver = Djikstra(DroneMap.start_hub, DroneMap.end_hub,
                                   DroneMap.hub)
    except ValidationError as e:
        print(e.errors()[0]['msg'].replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
