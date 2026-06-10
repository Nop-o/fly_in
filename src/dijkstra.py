from .hub import Hub
from .zone_type import ZoneType
from typing import Any
import heapq


class Dijkstra:
    def __init__(self, start: Hub, exit: Hub, hubs: dict[str, Any]) -> None:
        self.start: Hub = start
        self.exit: Hub = exit
        self.hubs: dict[str, Any] = hubs
        self.solution_path: dict[int, tuple[str, tuple[int, int]]] = {}

    def find_solution_and_update_hub_capacity(
            self) -> dict[int, tuple[str, tuple[int, int]]]:
        """
        Find the shortest path between the entry and the exit.
        If two paths take the same time, take the one with the
        highest priority.
        """
        solution: dict[str, Any] = self._find_solution()
        self._get_solution_path(solution)

        self._update_hub_connection_capacity()

        return self.solution_path

    def _get_solution_path(
            self, end_solution: dict[str, Any]) -> None:
        current: dict[str, Any] = end_solution

        while current is not None:
            self.solution_path[current["distance"]] = (current["hub_name"],
                                                       current["position"])

            stop_time = current.get("stop_time", 0)
            if current["previous"] is not None and stop_time > 0:
                for wait_turn in range(current["distance"] - stop_time,
                                       current["distance"]):
                    self.solution_path[wait_turn] = (
                        current["previous"]["hub_name"],
                        current["previous"]["position"]
                    )
            current = current["previous"]

    def _find_solution(self) -> dict[str, dict[str, Any]]:
        """
        Dijkstra algorithm:
            - on a graph, each points have a weight (init to inf)
            - the weight is the time cost the reach that point from start
            - if a new faster way of getting to a point is discovered,
              update the point weight
            - returns a dict with the current turn as a key and the position
              of the drone
        """
        solution: dict[str, dict[str, Any]] = {
            hub_name: {
                "distance": float('inf'),
                "position": None,
                "hub_name": None,
                "previous": None,
                "priority": None,
                "stop_time": 0,
             } for hub_name in self.hubs.keys()
            }
        queue = [(0, 0, 0, self.start)]

        solution[self.start.name]["distance"] = 0
        solution[self.start.name]["position"] = self.start.coordinates
        solution[self.start.name]["hub_name"] = self.start.name

        tie_breaker = 0

        while queue:
            distance, priority, new_tie_breaker, hub = heapq.heappop(queue)
            if distance > solution[hub.name]["distance"]:
                continue

            for neighbor in hub.neighbors:
                new_distance = distance + neighbor["hub"].get_hub_weight()
                stop_time = Dijkstra._get_stop_time(
                    hub, neighbor, new_distance,
                    solution[neighbor["hub"].name]["distance"]
                )
                new_distance += stop_time

                if Dijkstra._is_the_new_path_better(
                       new_distance, priority, solution[neighbor["hub"].name]):

                    tie_breaker += 1
                    new_priority = priority
                    if neighbor["hub"].zone == ZoneType.PRIORITY:
                        new_priority -= 1

                    solution[neighbor["hub"].name]["distance"] = new_distance
                    solution[neighbor["hub"].name]["previous"] = solution[
                        hub.name]
                    solution[neighbor["hub"].name]["position"] = neighbor[
                        "hub"].coordinates
                    solution[neighbor["hub"].name]["hub_name"] = neighbor[
                        "hub"].name
                    solution[neighbor["hub"].name]["priority"] = new_priority
                    solution[neighbor["hub"].name]["stop_time"] = stop_time

                    heapq.heappush(queue, (new_distance, new_priority,
                                           tie_breaker, neighbor["hub"]))

        return solution[self.exit.name]

    def _update_hub_connection_capacity(self) -> None:
        """Update hub/connection drone count when the drone is visiting it."""
        last_hub: Hub = self.start

        for turn in sorted(self.solution_path.keys()):
            hub = self.hubs[self.solution_path[turn][0]]

            hub.update_current_drone_count(turn)

            if last_hub != hub:
                neighbor = next(
                    n for n in last_hub.neighbors
                    if n["hub"].name == hub.name
                )
                if hub.zone == ZoneType.RESTRICTED:
                    neighbor["connection"].update_current_drone_count(turn - 2)
                neighbor["connection"].update_current_drone_count(turn - 1)

            last_hub = hub

    @staticmethod
    def _get_stop_time(hub: Hub, neighbor: dict[str, Any],
                       distance: int, shortest_distance: int
                       ) -> int | float:
        """Find the cost of traveling to the next hub."""
        stop_time: int | float = 0

        if neighbor["hub"].zone == ZoneType.BLOCKED:
            return float('inf')
        if (neighbor["hub"].max_drones == 0 or
           neighbor["connection"].max_link_capacity == 0):
            return float('inf')

        while not (neighbor["hub"].is_hub_accessible(distance + stop_time)
                   and neighbor["connection"].is_connection_accessible(
                    distance + stop_time - 1)
                   and (neighbor["hub"].zone != ZoneType.RESTRICTED or
                   neighbor["connection"].is_connection_accessible(
                    distance + stop_time - 2))):
            if (distance + stop_time) > shortest_distance:
                return float('inf')
            stop_time += 1
        return stop_time

    @staticmethod
    def _is_the_new_path_better(new_distance: int, new_priority: int,
                                best_solution: dict[str, int]) -> bool:
        """Decide if the new path is better than the current best one"""
        if new_distance == float('inf'):
            return False
        if new_distance == best_solution["distance"]:
            return new_priority < best_solution["priority"]
        return new_distance < best_solution["distance"]
