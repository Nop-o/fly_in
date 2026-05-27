from hub import Hub
from zone_type import ZoneType


class Dijkstra:
    def __init__(self, entry: Hub, exit: Hub) -> None:
        self.entry: Hub = entry
        self.exit: Hub = exit
        self.score: int = -1
        self.possible_solutions: list[list[Hub]] = []
        self.solution: list[Hub] = self.get_solution()

    def get_solution(self) -> list[Hub]:
        """
        Find the shortest path between the entry and the exit.
        If two paths take the same time, take the one with the
        highest priority.
        """
        solution: list[Hub] = []

        self.find_all_solutions(solution, self.entry, turn=0, score=0)
        solution = self.find_highest_priority_solution()
        self.update_hub_capacity(solution)

        return solution

    def find_highest_priority_solution(self) -> list[Hub]:
        solutions_with_equal_len: list[list[Hub]]
        if not self.possible_solutions:
            return []

        if len(self.possible_solutions) > 1:
            for i in range(len(self.possible_solutions[0])):
                for path in solutions_with_equal_len: 
                    if path[i].zone_type == ZoneType.PRIORITY:
                        return path
        return solutions_with_equal_len[0]

    def find_all_solutions(self, solution: list[Hub],
                           current_hub: Hub, turn: int, score: int) -> None:
        """
        Dijkstra algorithm:
            - on a map, each connections and points have a weight
            - the weight is the time cost the reach that point
            - it finds the shortest path between two points with a weighted map
        """
        if not current_hub or current_hub.zone_type == ZoneType.BLOCKED:
            return

        solution.append(current_hub)
        if current_hub.zone_type == ZoneType.RESTRICTED:
            score += 2
        else:
            score += 1

        if self.score != -1 and score > self.score:
            return

        if current_hub == self.exit:
            if score < self.score:
                self.possible_solutions.clear
                self.score = score
            self.possible_solutions.append(list(solution))
            solution.pop()
            return

        turn += 1

        for next_hub in current_hub.connections:
            while not Dijkstra.is_hub_free(next_hub, turn):
                solution.append(current_hub)
                turn += 1
                score += 1
            self.find_all_solutions(solution, next_hub, turn, score)

        solution.pop()

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
