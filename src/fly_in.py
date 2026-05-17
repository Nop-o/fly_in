from parsing import ValidateData
from drone_map import DroneMap
from pydantic import ValidationError


def main() -> None:
    try:
        file_content: ValidateData = ValidateData("test.txt")
        parsed_data = file_content.parse_file_content()
        drone_map = DroneMap(**parsed_data)
        drone_map.create_drones()
    except ValidationError as e:
        print(e.errors()[0]['msg'].replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
