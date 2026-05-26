from hub import Hub
from zone_type import ZoneType
from collections import deque


class Dijkstra:
    def __init__(self, entry: Hub, exit: Hub, id: int) -> None:
        self.entry: Hub = entry
        self.exit: Hub = exit
        self.possible_solutions: list[list[Hub | int]] = []
        self.solution: list[Hub] = self.get_solution(id)

    def get_solution(self, id: int) -> None:
        """
        Find the shortest path between the entry and the exit.
        If two paths take the same time, take the one with the
        highest priority.
        """
        solution: list[Hub] = []

        self.find_all_solutions(id, solution, self.entry, 0)
        solution = self.find_shortest_solution()
        self.update_hub_capacity(solution)

        return solution

    def find_shortest_solution(self) -> list[Hub]:
        solution_with_equal_len: list[List[Hub]]
        if not self.possible_solutions:
            return []

        min_length = min(map(self.possible_solutions[:-1]))

        solution_with_equal_len = [solution for solution
                                   in self.possible_solutions
                                   if len(solution) == min_length]

        if len(solution_with_equal_len) > 1:
            for i, solution in enumerate(solution_with_equal_len[0:-1], 0):
                if solution[i] == ZoneType.PRIORITY:
                    return solution
        return solution_with_equal_len[0]

    def find_all_solutions(self, id: int, solution: list[Hub],
                           current_hub: Hub, turn: int) -> None:
        """
        Dijkstra algorithm:
            - on a map, each connections and points have a weight
            - the weight is the time cost the reach that point
            - it finds the shortest path between two points with a weighted map
        """
        if not current_hub or current_hub.zone_type == BLOCKED:
            return

        solution.append(current_hub)
        if current_hub.zone_type == RESTRICTED:
            score += 2
        else:
            score += 1

        if current_hub == self.exit:
            self.possible_solutions.append(solution)
            update_path_score(solution)
            return

        turn += 1

        for next_hub in current_hub.connections:
            while next_hub.get_drone_capacity_per_turn(turn) >= next_hub.max_drones:
                turn += 1
                score += 1
            Dijkstra.find_all_solutions(id, solution, next_hub, turn)

    @staticmethod
    def update_hub_capacity(hub_list: list[Hub]) -> None:
        """Update all hub capacity when the drone is visiting it."""
        for i, hub in enumerate(hub_list, 0):
            hub.set_drone_capacity_per_turn(i)

            #next_hub = self.get_next_move(self.entry)
            #if not next_hub:
            #    break

            #if (next_hub.max_drones <= 
            #   next_hub.get_drone_capacity_per_turn(current_turn)):
            #    current_turn += hub.wait_your_turn()
                
            #if ((not self.lowest_move_path or
            #   lowest_move_path < self.lowest_move_path)
            #   and current_hub == self.exit):
            #    self.solution = solution
            #    self.lowest_move_path = lowest_move_path

            #solution.append[current_hub]

    #def find_shortest_path(self, id: int, hubs: list[Hub]) -> list[Hub] | None:
    #    """
    #    Dijkstra algorithm:
    #        - on a map, each connections and points have a weight
    #        - the weight is the time cost the reach that point
    #        - it finds the shortest path between two points with a weighted map
    #    """
    #    solution: dict[str, Hub] = {"turn_0": self.entry}
    #    visited_hub : set[Hub] = {Hub}
    #    queue: deque[Hub] = deque(self.entry)

    #    while hubs:
    #        current_hub = queue.popleft()
    #        if current_hub == self.exit:
    #            return solution
    #        for neighbor in current_hub.connections:
    #            if neighbor not in visited_hub:
    #                visited_hub.add(neighbor)
    #                if neighbor.zone_type != ZoneType.BLOCKED:
    #                    solution[neighbor] = current_hub
    #                    queue.append(neighbor)

    #    return None

    #def get_next_hub(self, current_hub: Hub) -> Hub | None:
    #    """Get to the nearest hub if there is one or wait a turn."""
    #    next_hub = Dijkstra.find_highest_priority_hub(current_hub.connections)

    #    if not next_hub or next_hub.zone_type == ZoneType.BLOCKED:
    #        return None

    #    if next_hub.get_drone_capacity_per_turn() >= next_hub.max_drones:
    #        return current_hub
    #    return next_hub

    #@staticmethod
    #def find_highest_priority_hub(hubs: list[Hub]) -> Hub:
    #    """Select the hub with the highest priority"""
    #    current_choice : Hub = None
    #    if not hubs:
    #        return current_choice

    #    for hub in hubs:
    #        if current_choice == None:
    #            current_choice = hub
    #        elif hub.zone_type.value < current_choice.zone_type.value:
    #            current_choice = hub
    #    return current_choice