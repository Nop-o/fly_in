from pydantic import BaseModel, Field, ValidationError, modelvalidator
from hub import Hub
from connection import Connection
from typing import Optional

class DroneMap(BaseModel):
    nb_drones: int = Field(ge=1)
    start_hub: Hub
    end_hub: Hub
    hub: Optional[list[Hub]]
    connection: Optional[list[Connection]]


def main() -> None:
    try:
        drone_map = DroneMap(
            nb_drones=5,
            start_hub=Hub(hub_type="normal", zone_name="start", x=0, y=0),
            end_hub=Hub(hub_type="norml", zone_name="goal", x=1, y=1),
            connection=Connection(zone_1_name="zone1",
                                  zone_1_name="zone2",
                                  max_link_capacity=2,)
        )
    except ValidationError as e:
        print(e.errors()[0]['msg'].replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()