from hub import Hub
from zone_type import ZoneType


class Djikstra:
    def __init__(self, entry: Hub, exit: Hub,
                 unvisited_hub: list[Hub]) -> None:
        self.entry = entry
        self.exit = exit
        self.unvisited_hub = unvisited_hub
    
    def find_shortest_path(self, id: int) -> list[Hub]:
        pass

    def get_next_move(self, current_hub: Hub) -> Hub | None:
        hub_choice: Hub = None

        for hub in current_hub.connections:
            if hub in unvisited_hub:
                if not hub_choice:
                    hub_choice = unvisited_hub
                else:
                    hub_choice = Djikstra.find_priority_hub(hub_choice, hub)

        if not hub_choice or hub_choice.zone_type == ZoneType.BLOCKED:
            return None
        return hub_choice

    @static_method
    def find_priority_hub(hub_1, hub_2) -> Hub:
        if hub_1.zone_type == ZoneType.PRIORITY:
            return hub_1
        elif hub_2.zone_type == ZoneType.PRIORITY:
            return hub_2
        elif hub_1.zone_type == ZoneType.NORMAL:
            return hub_1
        elif hub_2.zone_type == ZoneType.NORMAL:
            return hub_2
        elif hub_1.zone_type == ZoneType.RESTRICTED:
            return hub_1
        else:
            return hub_2
