class Parsing:
    def __init__(self, file_name: str) -> None:
        self.file_content: list[str] = Parsing.get_file_content(file_name)

    @staticmethod
    def get_file_content(file_name: str) -> list[str]:
        with open(file_name, "r") as file:
            content = file.readlines()

        file_content = [line.strip("\n") for line in content]
        return file_content

    def verify_file_content(self) -> None:
        possible_key: list[str] = [
            "nb_drones",
            "start_hub",
            "end_hub",
            "hub",
            "connection",
        ]
        zone_name: list[str] = []
        first: int = 1

        for i, line in enumerate(self.file_content):
            if not line or line[0] == "#":
                continue
            if ":" not in line:
                raise ValueError("Wrong file input: missing ':' "
                                 f"separator (line {i})")

            key, value = line.split(":", 1)

            if not key:
                raise ValueError("Wrong file input: no key given "
                                 f"(line {i})")
            if not value.strip() and value != '0':
                raise ValueError("Wrong file input: no value given "
                                 f"(line {i})")

            if key not in possible_key:
                if key in ["nb_drones", "start_hub", "end_hub"]:
                    raise ValueError(f"Wrong file input: {key} already used "
                                     f"(line {i})")
                raise ValueError(f"Wrong file input: {key} is not a value "
                                 f"key (line {i})")

            if key in ["nb_drones", "start_hub", "end_hub"]:
                if key == "nb_drones" and first != 1:
                    ValueError(
                        "Wrong file input: the number of drone is not the "
                        f"first input (line {i})"
                    )
                possible_key.remove(key)
            first = 0

            if key == "connection":
                Parsing.verify_connection(zone_name, key, value, i)
            elif key != "nb_drones":
                Parsing.verify_hubs(zone_name, key, value, i)

        possible_key.remove("hub")
        possible_key.remove("connection")
        if possible_key:
            raise ValueError(
                f"Wrong file input: missing {', '.join(possible_key)} key"
            )

    @staticmethod
    def verify_connection(zone_name: list[str], key: str,
                          input: str, line: int) -> None:
        if "-" not in input:
            raise ValueError(
                "Wrong file input: missing a dashe for a connection "
                f"format (line {line})"
            )

        split_data = input.strip().split("-")
        if (len(split_data) != 2):
            raise ValueError(
                "Wrong file input: two many dashes in a connection "
                f"(line {line})"
            )

        zone1, zone2 = split_data[0], split_data[1]
        if " " in zone2:
            split_metadata = zone2.split(" ")
            zone2, metadata = split_metadata[0], split_metadata[1]
            if (len(split_metadata) != 2):
                raise ValueError(
                    "Wrong file input: too many arguments for a connection "
                    f"(line {line})"
                )
            Parsing.verify_metadata(key, metadata, line)

        if zone1 not in zone_name or zone2 not in zone_name:
            raise ValueError(
                "Wrong file input: a hub needs to exist before connecting "
                f"(line {line})"
            )
        if zone1 == zone2:
            raise ValueError(
                "Wrong file input: a hub can't be connected to himself "
                f"(line {line})"
            )

    @staticmethod
    def verify_hubs(zone_name: list[str], key: str,
                    input: str, line: int) -> None:
        if " " not in input:
            raise ValueError(
                f"Wrong file input: not enough data given (line {line})"
            )

        data = input.strip().split(" ", 3)
        name, x, y = data[0], data[1], data[2]
        if len(data) == 4:
            metadata = data[3]
            Parsing.verify_metadata(key, metadata, line)

        if not name or (not x and x != '0') or (not y and y != '0'):
            raise ValueError(
                f"Wrong file input: not enough data given (line {line})"
            )

        if "-" in name:
            raise ValueError(
                f"Wrong file input: name can't have dashes (line {line})"
            )
        if name in zone_name:
            raise ValueError(
                "Wrong file input: can't have duplicate zone name"
                f"(line {line})"
            )
        zone_name.append(name)

    @staticmethod
    def verify_metadata(key: str, metadatas: str, line: int) -> None:
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

        list_metadata = metadatas[1: -1].split(" ")
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
            if ((m_key == "max_link_capacity" and key != "connection") or
               (m_key != "max_link_capacity" and key == "connection")):
                raise ValueError(
                    f"Wrong file input: a {key} doesn't have access to {m_key}"
                    f" metadata (line {line})"
                )
            if not m_value:
                raise ValueError(
                    f"Wrong file input: empty metadata value (line {line})"
                )
            possible_key.remove(m_key)


def main() -> None:
    try:
        file = Parsing("test.txt")
        file.verify_file_content()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
