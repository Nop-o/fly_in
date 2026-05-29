from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional
from drone import Drone
from hub import Hub
from connection import Connection


class DroneMap(BaseModel):

    nb_drones: int = Field(ge=1)
    start_hub: Hub
    end_hub: Hub
    hub: Optional[dict[str, Hub]]
    connection: Optional[list[Connection]]

    @model_validator(mode='after')
    def update_hub_neighbors(self) -> "DroneMap":
        """Verify if there is connections duplicate"""
        for connection in self.connection:
            if (connection.zone_2_name not in hub[connection.zone_1_name] and
               connection.zone_1_name not in hub[connection.zone_2_name]):
                self.hub[connection.zone_1_name].add(connection.zone_2_name)
                self.hub[connection.zone_2_name].add(connection.zone_1_name)
            else:
                raise ValueError("Connection error: multiple connections are "
                                 f"between {connection.zone_1_name} and "
                                 f"{connection.zone_2_name}")
        return self

    @model_validator(mode='after')
    def verify_entry_exit_max_drones(self) -> "DroneMap":
        """Verify if entry/exit can support all the drones at once"""
        if self.nb_drones > self.start_hub.max_drones:
            raise ValueError("Hub error: start hub can't support "
                             f"{self.nb_drones} drones")
        if self.nb_drones > self.end_hub.max_drones:
            raise ValueError("Hub error: end hub can't support "
                             f"{self.nb_drones} drones")
        return self

    # @model_validator(mode='after')
    # def update_all_connected_hub(self) -> None:
    #     """Connect all hubs based on their connections"""
    #     for connection in DroneMap.connection:
    #         self.hub[connection.zone_1_name]["connections"] = {
    #             connection.zone_2_name: connection}

    # def create_drones(self) -> None:
    #     """Call the drone factory to create the drones"""
    #     self.drones = Drone.drone_factory(self.nb_drones)

    # def update_all_solution(self) -> None:
    #     """Get the drones shortest path from entry to exit"""
    #     for drone in self.drones:
    #         drone.get_path_solution(drone.id)

    # def simulate_turn(self) -> None:
    #     """Simulate a turn for all drones"""
    #     for drone in self.drones:
    #         drone.simulate_turn()

    # def simulate_reverse_turn(self) -> None:
    #     """Simulate a reverse turn for all drones"""
    #     for drone in self.drones:
    #         drone.simulate_reverse_turn()
    
    # def visual_simulation(self) -> None:
    #     """Launch the visual representation of the simulation"""
    #     import pygame
        
    #     pygame.init()
    #     screen = pygame.display.set_mode((800, 600))
    #     clock = pygame.time.Clock()

    #     running = True
    #     while running:
    #         for event in pygame.event.get():
    #             if event.zone == pygame.QUIT:
    #                 running = False
            
    #         keys = pygame.key.get_pressed()
    #         if keys[pygame.K_LEFT]:
    #             self.simulate_reverse_turn()
    #         if keys[pygame.K_RIGHT]:
    #             self.simulate_turn()
            
    #         pygame.display.flip()
    #         clock.tick(60)

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
            ),
            end_hub=Hub(
                hub_type="normal",
                name="goal",
                coordinates=['4', '2'],
                zone="normal",
                color="red",
                max_drones=50,
            ),
            hub={"hub1": Hub(
                name="hub1",
                coordinates=['4', '1'],
                zone="normal",
                color="red",
                max_drones=50,
            )},
            connection=list[
                Connection(
                    zone_1_name="zone1",
                    zone_2_name="zone2",
                    max_link_capacity=2,
                ),
                Connection(
                    zone_1_name="zone2",
                    zone_2_name="zone3",
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
