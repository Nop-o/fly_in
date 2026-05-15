from pydantic import BaseModel, Field, ValidationError


class Connection(BaseModel):
    zone_1_name: str = Field(min_length=3, max_length=20)
    zone_2_name: str = Field(min_length=3, max_length=20)
    max_link_capacity: int = Field(default=1, ge=0)


def main() -> None:
    try:
        connection = Connection(
            zone_1_name="zone1",
            zone_2_name="zone2",
        )
        print(connection.zone_1_name)
        print(connection.zone_2_name)
        print(connection.max_link_capacity)
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
