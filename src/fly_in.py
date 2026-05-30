def main() -> None:
    try:
        from pydantic import ValidationError
    except ModuleNotFoundError:
        print("Import error: pydantic is not installed, run the "
              "'make install' command first")
        return

    from parsing import ValidateData
    from drone_map import DroneMap

    try:
        file_content: ValidateData = ValidateData("test.txt")
        parsed_data = file_content.parse_file_content()
        drone_map = DroneMap(**parsed_data)
        drone_map.create_drones()
        print(drone_map.drones)
        print(len(drone_map.drones))
    except ValidationError as e:
        print(e.errors()[0]['msg'].replace("Value error, ", ""))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
