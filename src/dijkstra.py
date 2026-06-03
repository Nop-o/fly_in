from hub import Hub
from zone_type import ZoneType
from typing import Any
import heapq


class Dijkstra:
    def __init__(self, start: Hub, exit: Hub) -> None:
        self.start: Hub = start
        self.exit: Hub = exit
        self.solution_path: tuple[str, tuple[int, int]] = {}

    def find_solution_and_update_hub_capacity(self, hubs: list[Hub]) -> None:
        """
        Find the shortest path between the entry and the exit.
        If two paths take the same time, take the one with the
        highest priority.
        """
        solutions: dict[str, dict[str, Any]] = self.find_solution(hubs)
        self.get_solution_path(solutions)
        self.update_hub_connection_capacity(hubs)

        return self.solution_path

    def get_solution_path(
            self, end_solution: dict[str, dict[str, Any]]) -> None:
        current: dict[str, Any] = end_solution

        while current is not None:
            self.solution_path[current["distance"]] = [current["hub_name"],
                                                       current["position"]]
            current = current["previous"]

    def find_solution(self, hubs: dict[str, Hub]) -> dict[str, dict[str, Any]]:
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
             } for hub_name in hubs.keys()
            }
        queue = [(0, 0, 0, self.start)]

        solution[self.start.name]["distance"] = 0
        solution[self.start.name]["position"] = self.start.coordinates
        solution[self.start.name]["hub_name"] = self.start.name

        while queue:
            distance, priority, tie_breaker, hub = heapq.heappop(queue)
            if distance > solution[hub.name]["distance"]:
                continue

            for neighbor in hub.neighbors:
                stop_time = Dijkstra.get_stop_time(
                        hub, neighbor, distance,
                        solution[neighbor["hub"].name]["distance"])

                new_distance = (distance + stop_time
                                + neighbor["hub"].get_hub_weight())

                if Dijkstra.is_the_new_path_better(
                       new_distance, priority, solution[neighbor["hub"].name]):

                    if neighbor["hub"].zone == ZoneType.PRIORITY:
                        priority -= 1

                    solution[neighbor["hub"].name]["distance"] = new_distance
                    solution[neighbor["hub"].name]["previous"] = solution[
                        hub.name]
                    solution[neighbor["hub"].name]["position"] = neighbor[
                        "hub"].coordinates
                    solution[neighbor["hub"].name]["hub_name"] = neighbor[
                        "hub"].name
                    tie_breaker += 1

                    heapq.heappush(queue, (new_distance, priority, tie_breaker,
                                           neighbor["hub"]))

        return solution[self.exit.name]

    @staticmethod
    def get_stop_time(hub: Hub, neighbor: dict[str, Any],
                      distance: int, shortest_distance: int
                      ) -> int | float:
        """Find the cost of traveling to the next hub."""
        stop_time: int | float = 0

        if neighbor["hub"].zone == ZoneType.BLOCKED:
            return float('inf')
        if (neighbor["hub"].max_drones == 0 or
           neighbor["connection"].max_link_capacity == 0):
            return float('inf')

        if shortest_distance == float('inf'):
            return 0

        while (distance + stop_time) <= shortest_distance:
            if neighbor["connection"].is_connection_accessible(distance +
                                                               stop_time):
                if neighbor["hub"].is_hub_accessible(distance + stop_time):
                    break
            stop_time += 1
        return stop_time

    def update_hub_connection_capacity(self, hubs: list[Hub]) -> None:
        """Update hub/connection drone count when the drone is visiting it."""
        turn: int = 0
        last_hub: Hub | None = None

        while turn in self.solution_path.keys():
            hub = hubs[self.solution_path[turn][0]]

            hub.update_current_drone_count(turn)
            if hub.zone == ZoneType.RESTRICTED and turn != 0:
                if last_hub != hub:
                    neighbor = next(
                        n for n in last_hub.neighbors
                        if n["hub"].name == hub.name
                    )
                    neighbor["connection"].update_current_drone_count(turn - 1)

            turn += 1
            last_hub = hub

    @staticmethod
    def is_the_new_path_better(new_distance: int, new_priority: int,
                               best_solution: dict[str, Any]) -> bool:
        """Decide if the new path is better than the current best one"""
        if new_distance == float('inf'):
            return False
        if new_distance == best_solution["distance"]:
            return new_priority < best_solution["priority"]
        return new_distance < best_solution["distance"]
