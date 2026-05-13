from pydantic import BaseModel, Field, ValidationError, modelvalidator
from typing import Optional


class Hub(BaseModel):
    hub_type: str = Field(default=normal, min_length=4, max_length=10)
    zone_name: str = Field(min_length=3, max_length=20)
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    zone: Optional[str] = Field(default=normal, min_length=6, max_length=10)
    color: Optional[str] = Field(default=None, min_length=3, max_length=20)
    max_drones: Optional[int] = Field(default=1, ge=0)


def main() -> None:
    try:
        hub = Hub(hub_type="normal", zone_name="z1h1", x=0, y=0)
        print(hub)
    except ValidationError as e:
        print(e.errors()[0]['msg'].replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
