from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Any, Annotated
from connection import Connection
from zone_type import ZoneType


Coordinate = Annotated[int, Field(ge=0, le=200)]

class Hub(BaseModel):

    name: str = Field(min_length=3, max_length=20)
    coordinates: tuple[Coordinate, Coordinate]
    zone: ZoneType = Field(default=ZoneType.NORMAL)
    color: str = Field(default="red", min_length=3, max_length=20)
    max_drones: int = Field(default=1, ge=0)
    neighbors: set["Hub"] = Field(default_factory=set)


    @model_validator(mode='before')
    @classmethod
    def update_zone(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Update the hub zone zone"""
        hub_type = data.get("zone", "normal")
        if hub_type == "normal":
            data["zone"] = ZoneType.NORMAL
        elif hub_type == "blocked":
            data["zone"] = ZoneType.BLOCKED
        elif hub_type == "restricted":
            data["zone"] = ZoneType.RESTRICTED
        elif hub_type == "priority":
            data["zone"] = ZoneType.PRIORITY
        else:
            raise ValueError("Hub error: impossible zone zone for "
                             f"{data['name']}")
        return data

    def set_current_drone_capacity_per_turn(self, turn: int) -> None:
        """Update/set the number of drone on the hub at a given turn"""
        if self.turn_capacity[turn]:
            self.turn_capacity[turn] += 1
        else:
            self.turn_capacity[turn] = 1
    
    def get_current_drone_capacity_per_turn(self, turn: int) -> int:
        """Get the number of drone on the hub at a given turn"""
        if not self.turn_capacity[turn]:
            return 0
        else:
            return self.turn_capacity[turn]
    
    def get_hub_weight(self) -> int:
        """Get the weight of coming to the hub."""
        if self.zone in [ZoneType.NORMAL, ZoneType.PRIORITY]:
            return 1
        elif self.zone in ZoneType.PRIORITY:
            return 2
        return (float('inf'))

    def add_neighbors(self, hub: 'Hub') -> None:
       self.connections.append(hub)

    def get_neighbors(self) -> list['Connection']:
       return self.neighbors

Hub.model_rebuild()

def main() -> None:
    try:
        hub = Hub(name="z1h1", coordinates=[1, 0])
        print(hub.name)
        print(hub.zone.value)
        print(hub.coordinates)
        print(hub.color)
        print(hub.max_drones)
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
