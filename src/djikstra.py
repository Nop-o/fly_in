from hub import Hub
from zone_type import ZoneType


class Djikstra:
    def __init__(self, entry: Hub, exit: Hub,
                 unvisited_hub: list[Hub]) -> None:
        self.entry = entry
        self.exit = exit
        self.unvisited_hub = unvisited_hub

    def find_shortest_path(self, id: int) -> list[Hub]:
        solution: list[Hub] = []
        lowest_move_path = 0
        current_turn = 0
        current_hub = self.entry

        
        while current_hub != self.exit:
            solution.append[current_hub]
            current_turn += 1
            next_hub = self.get_next_move(self.entry)
            if not next_hub:
                break
            if (next_hub.max_drones <= 
               next_hub.get_drone_capacity_per_turn(current_turn)):
                current_turn += hub.wait_your_turn()
                
            if ((not self.lowest_move_path or
               lowest_move_path < self.lowest_move_path)
               and current_hub == self.exit):
                self.solution = solution
                self.lowest_move_path = lowest_move_path
            
        
        return self.solution
            

    def get_next_move(self, current_hub: Hub) -> Hub | None:
        hub_choice: Hub = None

        for hub in current_hub.connections:
            if hub in self.unvisited_hub and hub.get_drone_capacity < hub.ma:
                if not hub_choice:
                    hub_choice = hub
                else:
                    hub_choice = Djikstra.find_priority_hub(hub_choice, hub)

        if not hub_choice or hub_choice.zone_type == ZoneType.BLOCKED:
            return None
        return hub_choice

    @staticmethod
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
