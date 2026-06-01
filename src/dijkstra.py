from hub import Hub
from connection import Connection
from zone_type import ZoneType
from typing import Any
import heapq


class Dijkstra:
    def __init__(self, start: Hub, exit: Hub) -> None:
        self.start: Hub = start
        self.exit: Hub = exit
        self.solution: dict[str, Any] = {
            "path": [],
            "score": 0}

    def find_solution_and_update_hub_capacity(self, hubs: list[Hub]) -> None:
        """
        Find the shortest path between the entry and the exit.
        If two paths take the same time, take the one with the
        highest priority.
        """
        self.solution = self.find_solution(hubs)
        self.update_hub_connection_capacity(self.solution)

        return self.solution

    def find_solution(self, hubs: dict[str, Hub]) -> dict[int, Hub | Connection]:
        """
        Dijkstra algorithm:
            - on a graph, each points have a weight (init to inf)
            - the weight is the time cost the reach that point from start
            - if a new faster way of getting to a point is discovered,
              update the point weight
            - returns a dict with the current turn as a key and the position
              of the drone
        """
        print("hello")
        print(hubs)
        solution: dict[str, dict[str, Any]] = {
            hub.name: {
                "turn": 0,
                "distance": float('inf'),
                "priority": 0,
                "path": [],
             } for hub in hubs
            }
        turn: int = 0
        queue = [(0, 0, self.start)]

        while queue:
            distance, priority, hub = heapq.heappop(queue)
            turn += 1

            if distance > solution[hub.name]["distance"]:
                continue

            for neighbor in hub.neighbors:
                weight = Dijkstra.get_travel_time(
                        hub, neighbor, turn, distance,
                        solution[neighbor.name]["distance"])
                turn += weight
                distance = distance + weight + neighbor.get_hub_weight()

                if Dijkstra.is_the_new_path_better(
                        distance, priority, solution[neighbor.name]):

                    if neighbor.zone_type == ZoneType.PRIORITY:
                        priority -= 1

                    solution[neighbor.name]["turn"] = turn
                    solution[neighbor.name]["distance"] = distance
                    solution[neighbor.name]["priority"] = priority
                    solution[neighbor.name]["path"].append(neighbor)

                    heapq.heappush(queue, (distance, priority, neighbor))

        return solution["path"][self.exit.name]

    @staticmethod
    def get_travel_time(hub: Hub, neighbor: Hub, turn: int,
                        distance: int, shortest_distance: int
                        ) -> int | float:
        """Find the cost of traveling to the next hub."""
        travel_time: int | float = 0
        connection: Connection = hub.neighbors[neighbor.name]["connection"]

        if neighbor.type == ZoneType.BLOCKED:
            return float('inf')
        if neighbor.max_drones == 0 or connection.max_link_capacity == 0:
            return float('inf')

        while (distance + travel_time) <= shortest_distance:
            if connection.is_connection_accessible(turn):
                if hub.is_hub_accessible(turn):
                    break
            turn += 1
            travel_time += 1

        return travel_time

    @staticmethod
    def is_the_new_path_better(new_distance: int, new_priority: int,
                               best_solution: dict[str, Any]) -> bool:
        """Decide if the new pqth is better thqn the current best one"""
        if new_distance == float('inf'):
            return False

        if new_distance == best_solution["distance"]:
            return new_priority < best_solution["priority"]
        return new_distance < best_solution["distance"]

    @staticmethod
    def update_hub_connection_capacity(
            path_solution: dict[int, Hub]) -> None:
        """Update hub/connection drone count when the drone is visiting it."""
        last_hub: Hub - None = None
        for turn, hub in path_solution.items():
            if hub.zone == ZoneType.RESTRICTED:
                 if last_hub and last_hub != hub:
                    last_hub["neighbors"]["connection"].update_current_drone_count(turn - 1)
            position.update_current_drone_count(turn)
