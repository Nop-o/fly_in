import heapq
from typing import Any, Optional
from zone_type import ZoneType

class Dijkstra:
    def __init__(self, entry: Any, exit: Any) -> None:
        self.entry = entry
        self.exit = exit
        self.solution: list[Any] = []

    def get_solution(self) -> None:
        # Priority Queue stores: (current_score, -priority_zones_count, path_list)
        # We use -priority_zones_count because heapq is a min-heap (lower is better)
        # so -2 is "better" than -1.
        queue = [(0, 0, [self.entry])]
        
        # Track the best score seen for each hub to prune inefficient paths
        best_scores: dict[str, int] = {}

        while queue:
            current_score, priority_count, path = heapq.heappop(queue)
            current_hub = path[-1]

            # Logic Error Fix: Check if we already found a better way to this hub
            if current_hub.id in best_scores and best_scores[current_hub.id] < current_score:
                continue
            best_scores[current_hub.id] = current_score

            # Goal reached
            if current_hub == self.exit:
                self.solution = path
                return

            for next_hub_id, connection in current_hub.connections.items():
                next_hub = connection.target_hub # Assuming Connection object access
                
                if next_hub.zone_type == ZoneType.BLOCKED:
                    continue

                # Calculate cost to move
                move_cost = 2 if next_hub.zone_type == ZoneType.RESTRICTED else 1
                new_score = current_score + move_cost
                new_priority_count = priority_count - (1 if next_hub.zone_type == ZoneType.PRIORITY else 0)

                # Wait logic: if hub/connection is full, increment score (turn) until free
                arrival_turn = new_score
                while not self.is_accessible(current_hub, next_hub, connection, arrival_turn):
                    arrival_turn += 1
                
                # Create a new path for this branch (prevents shared mutation)
                new_path = list(path) + [next_hub]
                heapq.heappush(queue, (arrival_turn, new_priority_count, new_path))

    def is_accessible(self, hub, next_hub, connection, turn) -> bool:
        """Helper to check both connection and hub capacity at a specific turn."""
        if connection.get_current_connection_capacity_per_turn(turn) >= connection.max_link_capacity:
            return False
        if next_hub.get_drone_capacity_per_turn(turn) >= next_hub.max_drones:
            return False
        return True