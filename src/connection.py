from pydantic import BaseModel, Field, ValidationError


class Connection(BaseModel):
    zone_1: str = Field(min_length=3, max_length=20)
    zone_2: str = Field(min_length=3, max_length=20)
    max_link_capacity: int = Field(default=1, ge=0, le=100)
    turn_capacity: int = Field(default=0)
    
    def set_current_connection_capacity_per_turn(self, turn: int) -> None:
        """Update/set the number of drone on the connection at a given turn"""
        if self.turn_capacity[turn]:
            self.turn_capacity[turn] += 1
        else:
            self.turn_capacity[turn] = 1
    
    def get_current_connection_capacity_per_turn(self, turn: int) -> int:
        """Get the number of drone on the connection at a given turn"""
        if not self.turn_capacity[turn]:
            return 0
        else:
            return self.turn_capacity[turn] 


def main() -> None:
    try:
        connection = Connection(
            zone_1="zone1",
            zone_2="zone2",
        )
        print(connection.zone_1)
        print(connection.zone_2)
        print(connection.max_link_capacity)
    except ValidationError as e:
        print(e.errors()[0]["msg"].replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
