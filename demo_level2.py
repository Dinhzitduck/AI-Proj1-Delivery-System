import demo_level1 as lv1
import numpy as np
def create_weight_array(array):
    weighted_edges = set()
    
    for row in range(len(array)):
        for col in range(len(array[0])):
            if array[row][col] != '-1':
                for delta_r, delta_c in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                    new_row, new_col = row + delta_r, col + delta_c
                    if 0 <= new_row < len(array) and 0 <= new_col < len(array[0]) and array[new_row][new_col] != 'S' and array[new_row][new_col] != 'G' and array[new_row][new_col] != '-1':
                        weight = int(array[new_row][new_col]) + 1
                        edge = lv1.WeightedEdge((row, col), (new_row, new_col), weight)
                        weighted_edges.add(edge)
    
    return list(weighted_edges)
    

def UCS_level_2(array, t):
    start = lv1.find_start(array)
    goal = lv1.find_goal(array)
    edges = create_weight_array(array)
    pq = [(0, start, [])]
    visited = set()
    
    while pq:
        cost, current, path = lv1.heapq.heappop(pq)
        
        if current in visited:
            continue
        
        path = path + [current]
        visited.add(current)
        if current == goal:
            if cost <= t:
                return path, cost
            else:
                return f"Doesn't exist a path that the car can go within {t} minute(s)", None
        
        for edge in edges:
            if edge.vertex1 == current and edge.vertex2 not in visited:
                lv1.heapq.heappush(pq, (cost + edge.weight, edge.vertex2, path))
            elif edge.vertex2 == current and edge.vertex1 not in visited:
                lv1.heapq.heappush(pq, (cost + edge.weight, edge.vertex1, path))

    return "Doesn't exist a path", None


array = [['S', '-1','-1', '0'],
         ['0', '10','0', '0'],
         ['0', '10','0', '0'],
         ['0', '-1','-1', 'G']]

    
path, cost = UCS_level_2(array,10)
if(cost is not None):
    print(f'Path is {path} with the cost of {cost}')
else: print(path)