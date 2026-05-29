from hub import Hub
from zone_type import ZoneType
from typing import Any
import heapq


class Dijkstra:
    def __init__(self, entry: Hub, exit: Hub) -> None:
        self.entry: Hub = entry
        self.exit: Hub = exit
        self.score: int = -1
        self.solution: dict[str, Any] = {}

    def get_solution(self) -> None:
        """
        Find the shortest path between the entry and the exit.
        If two paths take the same time, take the one with the
        highest priority.
        """
        solution: dict[str, Any] = {"path": [],
                                    "score": 0,}

        self.find_all_solutions(solution, self.entry, turn=0, score=0)
        self.update_hub_capacity(solution)

    def find_all_solutions(self, hubs: list[Hub], start_hub: Hub) -> None:
        """
        Dijkstra algorithm:
            - on a map, each connections and points have a weight
            - the weight is the time cost the reach that point
            - it finds the shortest path between two points with a weighted map
        """
        distance_from_start: {hub: float ('inf') for hub in hubs}
        distance_from_start[start_hub.name] = 0
        queue = [(0, start_hub.name)]

        while queue: 
            current_distance, current_hub = heapq.heappop(queue)
            if current_distance > distance_from_start[current_hub.zon]  