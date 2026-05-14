from parsing import ValidateData
from drone_map import DroneMap
from pydantic import ValidationError


def main() -> None:
    try:
        file_content: ValidateData = ValidateData("test.txt")
        parsed_data = file_content.parse_file_content()
        # print(parsed_data["nb_drones"])
        # print(parsed_data["start_hub"])
        # print(parsed_data["end_hub"])
        # print(parsed_data["hub"])
        # print(parsed_data["connection"])
        drone_map = DroneMap(**parsed_data)
        # print("\n\n")
        # print(drone_map.nb_drones)
        # print(drone_map.start_hub)
        # print(drone_map.end_hub)
        # print(drone_map.hub)
        # print(drone_map.connection)
    except ValidationError as e:
        print(e.errors()[0]['msg'].replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
