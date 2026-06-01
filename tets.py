import heapq 
 
def dijkstra(graph, start): 
    # Initialize distances and priority queue 
    distances = {node: float('inf') for node in graph} 
    distances[start] = 0 
    queue = [(0, start)] 
 
    while queue:
        print(f"queue : {queue}")
        current_distance, current_node = heapq.heappop(queue) 
 
        # Skip if we already found a shorter path 
        if current_distance > distances[current_node]: 
            continue 
 
        for neighbor, weight in graph[current_node].items(): 
            distance = current_distance + weight 
            if distance < distances[neighbor]: 
                distances[neighbor] = distance 
                heapq.heappush(queue, (distance, neighbor)) 
 
    return distances 
 
# Example graph 
graph = { 
    'A': {'B': 4, 'C': 4}, 
    'B': {'A': 4, 'C': 2}, 
    'C': {'A': 4, 'B': 2, 'D': 3, 'E': 1}, 
    'D': {'C': 3, 'F': 2},
    'E': {'C': 1, 'F': 3},
    'F': {'D': 2, 'E': 3},
} 
 
print(dijkstra(graph, 'A')) 
