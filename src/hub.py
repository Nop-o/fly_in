from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Any, Annotated
from zone_type import ZoneType


Coordinate = Annotated[int, Field(ge=-200, le=200)]


class Hub(BaseModel):

    name: str = Field(min_length=3, max_length=20)
    coordinates: tuple[Coordinate, Coordinate]
    zone: ZoneType = Field(default=ZoneType.NORMAL)
    color: str = Field(default="red", min_length=3, max_length=20)
    max_drones: int = Field(default=1, ge=0, le=100)
    neighbors: list[dict[str, Any]] = Field(default_factory=list)
    turn_capacity: dict[int, int] = Field(default_factory=dict)

    @model_validator(mode='before')
    @classmethod
    def _update_zone(cls, data: dict[str, Any]) -> dict[str, Any]:
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
            raise ValueError("Hub error: impossible zone type for "
                             f"{data['name']}")
        return data

    def update_current_drone_count(self, turn: int) -> None:
        """Update/set the number of drone on the hub at a given turn"""

        if turn not in self.turn_capacity.keys():
            self.turn_capacity[turn] = 1
        else:
            self.turn_capacity[turn] += 1

    def get_current_drone_count(self, turn: int) -> int:
        """Get the number of drone on the hub at a given turn"""
        if turn not in self.turn_capacity.keys():
            return 0
        return self.turn_capacity[turn]

    def get_hub_weight(self) -> int | float:
        """Get the weight of coming to the hub."""
        if self.zone in [ZoneType.NORMAL, ZoneType.PRIORITY]:
            return 1
        elif self.zone == ZoneType.RESTRICTED:
            return 2
        return (float('inf'))

    def is_hub_accessible(self, turn: int) -> bool:
        """See if a drone can access the hub."""
        return self.max_drones > self.get_current_drone_count(turn)


Hub.model_rebuild()


def main() -> None:
    try:
        hub = Hub(name="z1h1",
                  coordinates=(1, 0))
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
