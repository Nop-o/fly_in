from parsing import ValidateData
from drone_map import DroneMap


def main() -> None:
    try:
        from pydantic import ValidationError
    except ModuleNotFoundError:
        print("Import error: pydantic is not installed, run the "
                "'make install' command first")
        return

    try:
        file_content: ValidateData = ValidateData("src/test.txt")
        parsed_data = file_content.parse_file_content()
        drone_map = DroneMap(**parsed_data)
        drone_map.create_drones()
    except ValidationError as e:
        print(e.errors()[0]['msg'].replace("Value error, ", ""))

    drone_map.update_all_solution()
    print(drone)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
