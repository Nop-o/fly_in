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

        for line in self.file_content:
            if not line or line[0] == "#":
                continue
            if ":" not in line:
                raise ValueError("Wrong file input: missing ':' separator")

            key, value = line.split(":", 1)

            if not key:
                raise ValueError("Wrong file input: no key given")
            if not value.strip():
                raise ValueError(f"Wrong file input: no value given at {key}")

            if key not in possible_key:
                if key in ["nb_drones", "start_hub", "end_hub"]:
                    raise ValueError(f"Wrong file input: {key} already used")
                raise ValueError(f"Wrong file input: wrong key given '{key}'")

            if key in ["nb_drones", "start_hub", "end_hub"]:
                if key == "nb_drones" and first != 1:
                    ValueError(
                        "Wrong file input: the number of drone is not the first input"
                    )
                possible_key.remove(key)
            first = 0

            if key != "nb_drones":
                Parsing.verify_hubs(zone_name, value, key)

        possible_key.remove("hub")
        possible_key.remove("connection")
        if possible_key:
            raise ValueError(
                f"Wrong file input: missing {', '.join(possible_key)} key"
            )

    @staticmethod
    def verify_hubs(zone_name: list[str], input: str, key: str) -> None:
        if " " not in input:
            raise ValueError(
                f"Wrong file input: not enough data given at {key}"
            )

        data = input.split(" ")
        name, x, y = data[0], data[1], data[2]
        if len(data) == 4:
            metadata = data[3]
            Parsing.verify_metadata(key, metadata)

        if not name or not x or not y:
            raise ValueError(
                f"Wrong file input: not enough data given at {key}"
            )

        if "-" in name:
            raise ValueError(
                f"Wrong file input: name can't have dashes at {key}"
            )
        if name in zone_name:
            raise ValueError(
                f"Wrong file input: can't have duplicate zone name ({name})"
            )
        zone_name.append(name)

    @staticmethod
    def verify_metadata(key: str, metadatas: str) -> None:
        possible_key: list[str] = [
            "zone",
            "color",
            "max_drones",
            "max_link_capacity",
        ]

        if not metadatas.startswith("[") or not metadatas.endswith("]"):
            raise ValueError(
                f"Wrong file input: wrong metadata format at {key}"
            )

        list_metadata = metadatas.split(" ")
        for metadata in list_metadata:
            if not metadata or "=" not in metadata:
                raise ValueError(
                    f"Wrong file input: wrong metadata format at {key}"
                )

            m_key, m_value = metadata.split("=")
            if m_key not in possible_key:
                raise ValueError(
                    f"Wrong file input: {key} metadata key is not valid"
                )
            if m_key == "max_link_capacity" and key != "connection":
                raise ValueError(
                    f"Wrong file input: a {key} doesn't have access to 'max_link_capacity' metadata"
                )
            if not m_value:
                raise ValueError(
                    f"Wrong file input: empty metadata value at {m_key}"
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
