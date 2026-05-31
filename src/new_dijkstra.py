from hub import Hub
from connection import Connection
from zone_type import ZoneType
from typing import Any
import heapq


class Dijkstra:
    def __init__(self, start: Hub, exit: Hub) -> None:
        self.start: Hub = start
        self.exit: Hub = exit

    def get_solution(self, hubs: list(Hub)) -> None:
        """
        Find the shortest path between the entry and the exit.
        If two paths take the same time, take the one with the
        highest priority.
        """

        self.solution: dict[str, Any] = {"path": [],
                                         "score": 0,}

        self.solution = self.find_solutions(hubs)
        self.update_hub_capacity(solution)

    def find_solutions(self, hubs: list[Hub]) -> dict[str, Any]:
        """
        Dijkstra algorithm:
            - on a map, each connections and points have a weight
            - the weight is the time cost the reach that point
            - it finds the shortest path between two points with a weighted map
        """
        hubs_distances_from_start: dict[str, int] = {
            hub.name: float('inf') for hub in hubs}
        hubs_distances_from_start[self.start.name] = 0
        queue = [(0, 0, self.start)]
        current_turn: int = 0

        while queue: 
            current_distance, current_hub = heapq.heappop(queue)

            if current_distance > hubs_distances_from_start[current_hub.name]:
                continue
            
            for neighbor in current_hub.neighbors:
                distance = (current_distance +
                            Dijkstra.get_travel_time(current_hub, neighbor,
                                                     current_turn, ))

                if distance < hubs_distances_from_start[neighbor.name]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))
        
        return hubs_distances_from_start

    def get_travel_time(current_hub: Hub, neighbor: Hub, turn: int,
                        current_score: int, best_score : int 
                        ) -> int:
        time_spend: int = current_hub.get_hub_weight()
        connection : Connection = current_hub.neighbors[neighbor.name]["connection"]

        if neighbor.type == ZoneType.BLOCKED:
            return float('inf')

        while ((neighbor.max_drones <=
            neighbor.get_current_drone_capacity_per_turn(turn)
            or connection.max_drones <=
            connection.get_current_drone_capacity_per_turn(turn))
            and (current_score + time_spend) <= best_score):
                turn += 1
                time_spend += 1

        return time_spend
                
        
    @staticmethod
    def update_hub_capacity(hub_list: list[Hub]) -> None:
        """Update all hub capacity when the drone is visiting it."""
        for i, hub in enumerate(hub_list, 0):
            hub.set_drone_capacity_per_turn(i)
        
    @staticmethod
    def update_connection_capacity(connection_list: list[Hub]) -> None:
        """Update all hub capacity when the drone is visiting it."""
        for i, hub in enumerate(hub_list, 0):
            hub.set_drone_capacity_per_turn(i)
