from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Any
from connection import Connection
from zone_type import ZoneType


class Hub(BaseModel):

    zone_name: str = Field(min_length=3, max_length=20)
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    zone_type: ZoneType = Field(default=ZoneType.NORMAL)
    color: str = Field(default=None, min_length=3, max_length=20)
    max_drones: int = Field(default=1, ge=0)

    @model_validator(mode='before')
    @classmethod
    def update_zone(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Update the hub zone type"""
        if not data.get("zone_type"):
            data["zone_type"] = ZoneType.NORMAL
        elif data["zone_type"] == "normal":
            data["zone_type"] = ZoneType.NORMAL
        elif data["zone_type"] == "blocked":
            data["zone_type"] = ZoneType.BLOCKED
        elif data["zone_type"] == "restricted":
            data["zone_type"] = ZoneType.RESTRICTED
        elif data["zone_type"] == "priority":
            data["zone_type"] = ZoneType.PRIORITY
        else:
            raise ValueError("Hub error: impossible zone type for "
                             f"{data['zone_name']}")
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


def main() -> None:
    try:
        hub = Hub(zone_name="z1h1", x=1, y=0)
        print(hub.x)
        print(hub.y)
        print(hub.zone_name)
        print(hub.zone_type.value)
        print(hub.color)
        print(hub.max_drones)
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
