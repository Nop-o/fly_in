from __future__ import annotations
from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional
from drone import Drone
from hub import Hub
from connection import Connection


class DroneMap(BaseModel):

    nb_drones: int = Field(ge=1)
    start_hub: Hub
    end_hub: Hub
    hub: Optional[list[Hub]]
    connection: Optional[list[Connection]]

    @model_validator(mode='after')
    def verify_hub_coordonates_duplicate(self) -> DroneMap:
        """Verify if hubs have the same coordonates"""
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
    def verify_connection_duplicate(self) -> DroneMap:
        """Verify if there is connections duplicate"""
        for i in range(0, len(self.connection)):
            for j in range(i + 1, len(self.connection)):
                zones_1 = [self.connection[i].zone_1_name,
                           self.connection[i].zone_2_name]
                zones_2 = [self.connection[j].zone_1_name,
                           self.connection[j].zone_2_name]
                if all(element in zones_1 for element in zones_2):
                    raise ValueError("Connection error: multiple connections "
                                     "are between "
                                     f"{self.connection[i].zone_1_name} and "
                                     f"{self.connection[i].zone_2_name}")
        return self

    @model_validator(mode='after')
    def verify_entry_exit_max_drones(self) -> DroneMap:
        """Verify if entry/exit can support all the drones at once"""
        if self.nb_drones > self.start_hub.max_drones:
            raise ValueError("Hub error: start hub can't support "
                             f"{self.nb_drones} drones")
        if self.nb_drones > self.end_hub.max_drones:
            raise ValueError("Hub error: end hub can't support "
                             f"{self.nb_drones} drones")
        return self

    def update_all_connected_hub(self) -> None:
        """Link all hubs based on their connections"""
        for hub in self.hub:
            hub.update_hub_connected_hub(self)

    def update_connected_hub(self) -> None:
        """Link one hubs based on his connections"""
        for hub in self.hub:
            connected_hub: list[Hub] = []
            for connection in DroneMap.connection:
                if hub.zone_name == connection.zone_1_name:
                    connected_hub.append(get_hub(connection.zone_2_name))
                else:
                    connected_hub.append(get_hub(connection.zone_1_name))

            hub.update_hub_connection(connected_hub)
    
    def get_hub(self, hub_name: str) -> Hub:
        """Get an hub based on his zone_name"""
        for hub in self.hub:
            if hub_name == hub.zone_name:
                return hub

    def create_drones(self) -> None:
        """Call the drone factory to create the drones"""
        self.drones = Drone.drone_factory(self.nb_drones)

    def update_all_solution(self) -> None:
        """Get the drones shortest path from entry to exit"""
        for drone in self.drones:
            drone.get_path_solution(drone.id)

    def simulate_turn(self) -> None:
        """Simulate a turn for all drones"""
        for drone in self.drones:
            drone.simulate_turn()

    def simulate_reverse_turn(self) -> None:
        """Simulate a reverse turn for all drones"""
        for drone in self.drones:
            drone.simulate_reverse_turn()
    
    def visual_simulation(self) -> None:
        """Launch the visual representation of the simulation"""
        import pygame
        
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.simulate_reverse_turn()
            if keys[pygame.K_RIGHT]:
                self.simulate_turn()
            
            pygame.display.flip()
            clock.tick(60)


def main() -> None:
    try:
        drone_map = DroneMap(
            nb_drones=5,
            start_hub=Hub(
                hub_type="normal",
                zone_name="start",
                x=0,
                y=0,
                zone_type="normal",
                color="red",
                max_drones=50,
            ),
            end_hub=Hub(
                hub_type="normal",
                zone_name="goal",
                x=1,
                y=1,
                zone_type="normal",
                color="red",
                max_drones=50,
            ),
            hub=Hub(
                hub_type="normal",
                zone_name="hub1",
                x=0,
                y=1,
                zone_type="normal",
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
