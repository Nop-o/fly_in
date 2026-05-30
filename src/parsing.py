from typing import Any


class ValidateData:
    def __init__(self, file_name: str) -> None:
        self.file_content: list[str] = ValidateData.get_file_content(file_name)

    @staticmethod
    def get_file_content(file_name: str) -> list[str]:
        """Open the file given in argument and retriewe it's content"""
        with open(file_name, "r") as file:
            content = file.readlines()

        file_content = [line.strip("\n") for line in content]
        return file_content

    def parse_file_content(self) -> dict[str, Any]:
        """
        Verify if the retrieved data is in the food format and useable.
        Return a dict that will be used to create a drone map which contains
        hubs and connections who will be created at the same time as the map.
        """
        parsed_data: dict[str, Any] = {
            "nb_drones": 1,
            "start_hub": None,
            "end_hub": None,
            "hub": {},
            "connection": [],
            "drones": [],
        }

        possible_key: list[str] = [
            "nb_drones",
            "start_hub",
            "end_hub",
            "hub",
            "connection",
        ]
        zone_name: set[str] = set()
        coordinates: set[tuple[str, str]] = set()
        is_first: bool = True

        for i, line in enumerate(self.file_content):
            if not line or line[0] == "#":
                continue
            if "#" in line:
                line, comment = line.split("#", 1)
            if ":" not in line:
                raise ValueError(
                    "Wrong file input: missing ':' " f"separator (line {i})"
                )

            key, value = line.split(":", 1)

            if not key:
                raise ValueError(
                    "Wrong file input: no key given " f"(line {i})"
                )
            if not value.strip() and value != "0":
                raise ValueError(
                    "Wrong file input: no value given " f"(line {i})"
                )

            if key not in possible_key:
                if key in ["nb_drones", "start_hub", "end_hub"]:
                    raise ValueError(
                        f"Wrong file input: {key} already used " f"(line {i})"
                    )
                raise ValueError(
                    f"Wrong file input: {key} is not a value "
                    f"key (line {i})"
                )

            if key in ["nb_drones", "start_hub", "end_hub"]:
                possible_key.remove(key)
                if key == "nb_drones" and not is_first:
                    raise ValueError(
                        "Wrong file input: the number of drone is not the "
                        f"first input (line {i})"
                    )
            is_first = False

            if key == "connection":
                parsed_data[key].append(
                    ValidateData.verify_connection(zone_name, value, i)
                )
            elif key == "hub":
                new_hub = ValidateData.verify_hub(zone_name, coordinates,
                                                  key, value, i,
                                                  parsed_data["nb_drones"])
                parsed_data[key][new_hub["name"]] = new_hub
            elif key == "nb_drones":
                parsed_data[key] = value.strip()
            else:
                parsed_data[key] = ValidateData.verify_hub(
                                        zone_name, coordinates, key, value,
                                        i, parsed_data["nb_drones"])

        possible_key.remove("hub")
        possible_key.remove("connection")
        if possible_key:
            raise ValueError(
                f"Wrong file input: missing {', '.join(possible_key)} key"
            )
        return parsed_data

    @staticmethod
    def verify_connection(
        zone_name: set[str], value: str, line: int
    ) -> dict[str, str]:
        """Verify that the possible connection is valid."""
        connection: dict[str, str] = {
            "zone_1": None,
            "zone_2": None,
            "max_link_capacity": 1,
            "turn_capacity": {},
        }

        if "-" not in value:
            raise ValueError(
                "Wrong file input: missing a dashe for a connection "
                f"format (line {line})"
            )

        split_data = value.strip().split("-")
        if len(split_data) != 2:
            raise ValueError(
                "Wrong file input: two many dashes in a connection "
                f"(line {line})"
            )

        zone1, zone2 = split_data[0], split_data[1]
        if " " in zone2:
            split_metadata = zone2.split(" ")
            if len(split_metadata) != 2:
                raise ValueError(
                    "Wrong file input: too many arguments for a connection "
                    f"(line {line})"
                )
            zone2, metadata = split_metadata[0], split_metadata[1]
            connection.update(ValidateData.verify_metadata("connection",
                                                           metadata, line))
        connection["zone_1"] = zone1
        connection["zone_2"] = zone2

        if zone1 not in zone_name or zone2 not in zone_name:
            raise ValueError(
                "Wrong file input: a hub needs to exist before connecting it "
                f"(line {line})"
            )
        if zone1 == zone2:
            raise ValueError(
                "Wrong file input: a hub can't be connected to himself "
                f"(line {line})"
            )
        return connection

    @staticmethod
    def verify_hub(
        zone_name: set[str], coordinates: set[tuple[str, str]],
        key: str, value: str, line: int, drone_count: str
    ) -> dict[str, str]:
        """Verify that the possible hub is valid."""
        hub: dict[str, str] = {
            "name": None,
            "coordinates": None,
            "zone": "normal",
            "color": "red",
            "neighbors": [],
            "turn_capacity": {},
        }

        if " " not in value:
            raise ValueError(
                f"Wrong file input: not enough data given (line {line})"
            )

        data = value.strip().split(" ", 3)
        if (len(data) < 3 or not data[0] or (not data[1] and data[1] != "0") or
           (not data[2] and data[2] != "0")):
            raise ValueError(
                f"Wrong file input: not enough data given (line {line})"
            )

        hub["name"] = data[0]
        hub["coordinates"] = (data[1], data[2])
        if len(data) == 4:
            metadata = data[3]
            hub.update(ValidateData.verify_metadata(key, metadata, line))

        if key in ["start_hub", "end_hub"] and "max_drones" not in metadata:
            hub["max_drones"] = drone_count
        else:
            hub["max_drones"] = hub.get("max_drones", '1')

        if "-" in data[0]:
            raise ValueError(
                f"Wrong file input: name can't have dashes (line {line})"
            )
        if hub["name"] in zone_name:
            raise ValueError(
                "Wrong file input: can't have duplicate zone name"
                f"(line {line})"
            )
        if hub["coordinates"] in coordinates:
            raise ValueError(
                "Wrong file input: can't have duplicate coordinates"
                f"(line {line})"
            )
        zone_name.add(hub["name"])
        coordinates.add(hub["coordinates"])
        return hub

    @staticmethod
    def verify_metadata(key: str, metadatas: str, line: int) -> dict[str, str]:
        """Verify that the possible metadata is valid."""
        parsed_metadata: dict[str, str] = {}

        possible_key: list[str] = [
            "zone",
            "color",
            "max_drones",
            "max_link_capacity",
        ]
        if not metadatas.startswith("[") or not metadatas.endswith("]"):
            raise ValueError(
                f"Wrong file input: wrong metadata format (line {line})"
            )

        list_metadata = metadatas[1:-1].split(" ")
        for metadata in list_metadata:
            if not metadata or "=" not in metadata:
                raise ValueError(
                    f"Wrong file input: wrong metadata format (line {line})"
                )

            m_key, m_value = metadata.split("=")
            if m_key not in possible_key:
                raise ValueError(
                    f"Wrong file input: {key} metadata key is not valid "
                    f"(line {line})"
                )
            if (m_key == "max_link_capacity" and key != "connection") or (
                m_key != "max_link_capacity" and key == "connection"
            ):
                raise ValueError(
                    f"Wrong file input: a {key} doesn't have access to {m_key}"
                    f" metadata (line {line})"
                )
            if not m_value:
                raise ValueError(
                    f"Wrong file input: empty metadata value (line {line})"
                )

            parsed_metadata[m_key] = m_value
            possible_key.remove(m_key)
        return parsed_metadata


def main() -> None:
    try:
        file_content: ValidateData = ValidateData("test.txt")
        parsed_data = file_content.parse_file_content()
        print(parsed_data["nb_drones"])
        print(parsed_data["start_hub"])
        print(parsed_data["end_hub"])
        print(parsed_data["hub"])
        print(parsed_data["connection"])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
