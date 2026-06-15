from pydantic import BaseModel, Field, ValidationError, model_validator
from .drone import Drone
from .hub import Hub
from .connection import Connection
from .zone_type import ZoneType
import pygame


class DroneMap(BaseModel):

    nb_drones: int = Field(ge=1, le=100)
    start_hub: Hub
    end_hub: Hub
    hub: dict[str, Hub]
    connection: list[Connection]
    drones: list[Drone] = Field(default_factory=list)

    @model_validator(mode='after')
    def _add_start_end_hub_to_hub(self) -> "DroneMap":
        """"Add start/end hubs to DroneMap.hub"""
        self.hub[self.start_hub.name] = self.start_hub
        self.hub[self.end_hub.name] = self.end_hub
        return self

    @model_validator(mode='after')
    def _update_hub_neighbors(self) -> "DroneMap":
        """Verify if there is connections duplicate"""

        if not self.connection:
            raise ValueError("Connection error: no connections created")

        for road in self.connection:
            if (any(neighbor["hub"] == self.hub[road.zone_1]
                    for neighbor in self.hub[road.zone_2].neighbors) or
                any(neighbor["hub"] == self.hub[road.zone_2]
                    for neighbor in self.hub[road.zone_1].neighbors)):
                raise ValueError("Connection error: multiple connections are "
                                 f"between {road.zone_1} and "
                                 f"{road.zone_2}")
            else:
                self.hub[road.zone_1].neighbors.append({
                    "hub": self.hub[road.zone_2], "connection": road})
                self.hub[road.zone_2].neighbors.append({
                    "hub": self.hub[road.zone_1], "connection": road})
        return self

    def create_drones(self) -> None:
        """Call the drone factory to create the drones"""
        self.drones = Drone.drone_factory(self.nb_drones)

    def update_all_solution(self) -> None:
        """Get the drones shortest path from entry to exit"""
        for drone in self.drones:
            drone.get_path_solution(self.hub, self.start_hub, self.end_hub)

    def print_all_drone_position_and_id(self, turn: int) -> None:
        """Simulate a reverse turn for all drones"""
        for drone in self.drones:
            drone.print_current_position_and_id(turn)
        print("\n")


DroneMap.model_rebuild()


def main() -> None:

    try:
        drone_map = DroneMap(
            nb_drones=5,
            start_hub=Hub(
                name="start",
                coordinates=(4, 3),
                zone=ZoneType.NORMAL,
                color=pygame.Color("green"),
                max_drones=50,
            ),
            end_hub=Hub(
                name="goal",
                coordinates=(4, 2),
                zone=ZoneType.NORMAL,
                color=pygame.Color("green"),
                max_drones=50,
            ),
            hub={"hub1": Hub(
                name="hub1",
                coordinates=(4, 1),
                zone=ZoneType.NORMAL,
                color=pygame.Color("green"),
                max_drones=50,
            )},
            connection=[
                Connection(
                    zone_1="start",
                    zone_2="hub1",
                    max_link_capacity=2
                ),
                Connection(
                    zone_1="hub1",
                    zone_2="goal",
                    max_link_capacity=2,
                ),
            ],
            drones=[],
        )

        print(drone_map)
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
