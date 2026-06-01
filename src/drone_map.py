from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional
from drone import Drone
from hub import Hub
from connection import Connection


class DroneMap(BaseModel):

    nb_drones: int = Field(ge=1, le=100)
    start_hub: Hub
    end_hub: Hub
    hub: Optional[dict[str, Hub]]
    connection: Optional[list[Connection]]
    drones: Optional[list[Drone]] = Field(default_factory=list)

    @model_validator(mode='after')
    def add_start_end_hub_to_hub(self) -> "DroneMap":
        self.hub[self.start_hub.name] = self.start_hub
        self.hub[self.end_hub.name] = self.end_hub
        return self

    @model_validator(mode='after')
    def update_hub_neighbors(self) -> "DroneMap":
        """Verify if there is connections duplicate"""

        if not self.connection:
            raise ValueError("Connection error: no connections created")

        for road in self.connection:
            if (self.hub[road.zone_2].neighbors.get(road.zone_1) or
               self.hub[road.zone_1].neighbors.get(road.zone_2)):
                raise ValueError("Connection error: multiple connections are "
                                 f"between {road.zone_1} and "
                                 f"{road.zone_2}")
            else:
                self.hub[road.zone_1].neighbors[road.zone_2] = {
                    "hub": self.hub[road.zone_2], "connection": road}
                self.hub[road.zone_2].neighbors[road.zone_1] = {
                    "hub": self.hub[road.zone_1], "connection": road}
        return self

    @model_validator(mode='after')
    def verify_entry_exit_max_drones(self) -> "DroneMap":
        """Verify if entry/exit can support all the drones at once"""
        if self.nb_drones > self.start_hub.max_drones:
            raise ValueError("Hub error: start hub can't support "
                             f"{self.nb_drones} drones (only "
                             f"{self.start_hub.max_drones})")
        if self.nb_drones > self.end_hub.max_drones:
            raise ValueError("Hub error: end hub can't support "
                             f"{self.nb_drones} drones (only "
                             f"{self.end_hub.max_drones})")
        return self

    def create_drones(self) -> None:
        """Call the drone factory to create the drones"""
        self.drones = Drone.drone_factory(self.nb_drones, self.start_hub)

    def update_all_solution(self) -> None:
        """Get the drones shortest path from entry to exit"""
        for drone in self.drones:
            drone.get_path_solution(self.hub, self.start_hub, self.end_hub)

    def simulate_turn(self) -> None:
        """Simulate a turn for all drones"""
        for drone in self.drones:
            drone.simulate_turn()
        print()

    def simulate_reverse_turn(self) -> None:
        """Simulate a reverse turn for all drones"""
        for drone in self.drones:
            drone.simulate_reverse_turn()
        print()


DroneMap.model_rebuild()


def main() -> None:
    try:
        drone_map = DroneMap(
            nb_drones=5,
            start_hub=Hub(
                hub_type="normal",
                name="start",
                coordinates=['4', '3'],
                zone="normal",
                color="red",
                max_drones=50,
                neighbors={},
            ),
            end_hub=Hub(
                hub_type="normal",
                name="goal",
                coordinates=['4', '2'],
                zone="normal",
                color="red",
                max_drones=50,
                neighbors={},
            ),
            hub={"hub1": Hub(
                name="hub1",
                coordinates=['4', '1'],
                zone="normal",
                color="red",
                max_drones=50,
                neighbors={},
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
        print("hello")
        print(e)


if __name__ == "__main__":
    main()
