from hub import Hub
from zone_type import ZoneType
from typing import Any


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

    def find_all_solutions(self, solution: dict[str, Any],
                           current_hub: Hub, turn: int, score: int) -> None:
        """
        Dijkstra algorithm:
            - on a map, each connections and points have a weight
            - the weight is the time cost the reach that point
            - it finds the shortest path between two points with a weighted map
        """
        if not current_hub or current_hub.zone_type == ZoneType.BLOCKED:
            return

        solution["path"].append(current_hub)

        if current_hub.zone_type == ZoneType.RESTRICTED:
            solution["score"] += 2
        else:
            solution["score"] += 1

        if self.score != -1 and solution["score"] > self.score:
            return

        if current_hub == self.exit:
            self.score = solution["score"]
            self.find_highest_priority_solution(solution)
            solution["path"].pop()
            return

        turn += 1

        for next_hub in current_hub.connections:
            while (not Dijkstra.is_connection_free(next_hub, turn)
               or not Dijkstra.is_hub_free(next_hub, turn)):
                solution["path"].append(current_hub)
                solution["score"] += 1
                turn += 1
            self.find_all_solutions(solution, next_hub, turn, score)

        solution.pop()

    def find_highest_priority_solution(self, new_solution: dict[str, Any]) -> None:
        tie_breaker: dict[str, Any]
        if not self.solution:
            self.solution = solution
            return

        if len(self.solution["path"]) > len(new_solution["path"]):
            min_length =  len(new_solution["path"])
            tie_breaker = new_solution
        else:
            min_length =  len(self.solution["path"])
            tie_breaker = self.solution

        for i in range(min_length):
            if (self.solution["path"][i].zone_type == ZoneType.PRIORITY
               and new_solution["path"][i].zone_type != ZoneType.PRIORITY):
                return
            elif (new_solution["path"][i].zone_type == ZoneType.PRIORITY
               and self.solution["path"][i].zone_type != ZoneType.PRIORITY):
                return
        self.solution = tie_breaker

    @staticmethod
    def is_connection_free(hub: Hub, connexion: str, turn: int) -> bool:
        if hub["connexions"][] #fix this

    @staticmethod
    def is_hub_free(hub: Hub, turn: int) -> bool:
        if hub.zone_type == ZoneType.RESTRICTED:
            turn += 1

        if hub.get_drone_capacity_per_turn(turn) >= hub.max_drones:
            return False
        return True

    @staticmethod
    def update_hub_capacity(hub_list: list[Hub]) -> None:
        """Update all hub capacity when the drone is visiting it."""
        for i, hub in enumerate(hub_list, 0):
            hub.set_drone_capacity_per_turn(i)
