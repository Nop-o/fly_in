from pydantic import BaseModel, Field, ValidationError, model_validator
from hub import Hub
from connection import Connection
from typing import Optional


class DroneMap(BaseModel):
    nb_drones: int = Field(ge=1)
    start_hub: Hub
    end_hub: Hub
    hub: Optional[list[Hub]]
    connection: Optional[list[Connection]]

    @model_validator(mode='after')
    def verify_hub_coordonates_duplicate(self) -> 'DroneMap':
        for i in range(0, len(self.hub)):
            for j in range(i + 1, len(self.hub)):
                if (self.hub[i].x == self.hub[j].x and
                   self.hub[i].y == self.hub[j].y):
                    raise ValueError(f"Hub error: hubs {self.hub[i].zone_name}"
                                     f" and {self.hub[j].zone_name} have the "
                                     "same coordonates")

            if (self.start_hub.x == self.hub[i].x and
               self.start_hub.y == self.hub[i].y):
                raise ValueError(f"Hub error: hubs {self.start_hub.zone_name} "
                                 f"and {self.hub[i].zone_name} have the same "
                                 "coordonates")
            if (self.end_hub.x == self.hub[i].x and
               self.end_hub.y == self.hub[i].y):
                raise ValueError(f"Hub error: hubs {self.end_hub.zone_name} "
                                 f"and {self.hub[i].zone_name} have the same "
                                 "coordonates")

        if (self.end_hub.x == self.start_hub.x and
           self.end_hub.y == self.start_hub.y):
            raise ValueError(f"Hub error: hubs {self.end_hub.zone_name} "
                             f"and {self.start_hub.zone_name} have the "
                             "same coordonates")
        return self

    @model_validator(mode='after')
    def verify_connection_duplicate(self) -> 'DroneMap':
        for i in range(0, len(self.connection)):
            for j in range(i + 1, len(self.connection)):
                if ((self.connection[i].zone_1_name ==
                   self.connection[j].zone_1_name) and
                   (self.connection[i].zone_2_name ==
                   self.connection[j].zone_2_name)):
                    raise ValueError("Connection error: multiple connections "
                                     "are between "
                                     f"{self.connection[i].zone_1_name} and "
                                     f"{self.connection[i].zone_2_name}")
        return self

    @model_validator(mode='after')
    def verify_entry_exit_max_drones(self) -> 'DroneMap':
        if self.nb_drones > self.start_hub.max_drones:
            raise ValueError("Hub error: start hub can't support "
                             f"{self.nb_drones} drones")
        if self.nb_drones > self.end_hub.max_drones:
            raise ValueError("Hub error: end hub can't support "
                             f"{self.nb_drones} drones")
        return self


def main() -> None:
    try:
        drone_map = DroneMap(
            nb_drones=5,
            start_hub=Hub(
                hub_type="normal",
                zone_name="start",
                x=0,
                y=0,
                zone="normal",
                color="red",
                max_drones=50,
            ),
            end_hub=Hub(
                hub_type="normal",
                zone_name="goal",
                x=1,
                y=1,
                zone="normal",
                color="red",
                max_drones=50,
            ),
            hub=Hub(
                hub_type="normal",
                zone_name="hub1",
                x=0,
                y=1,
                zone="normal",
                color="red",
                max_drones=50,
            ),
            connection=list[
                Connection(
                    zone_1_name="zone1",
                    zone_2_name="zone2",
                    max_link_capacity=2,
                ),
            ],
        )
        print(drone_map)
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
