import random
import heapq

class WeightedEdge():
    def __init__(self, u, v, weight):
        self.vertex1 = u
        self.vertex2 = v
        self.weight = weight

    def __eq__(self, other):
        return (self.vertex1, self.vertex2) == (other.vertex1, other.vertex2) or \
               (self.vertex1, self.vertex2) == (other.vertex2, other.vertex1)

    def __hash__(self):
        return hash(frozenset([self.vertex1, self.vertex2]))
    
def create_random_weight_array(array):
    weighted_edges = []
    
    for row in range(len(array)):
        for col in range(len(array[0])):
            if array[row][col] != '-1':
                for delta_r, delta_c in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                    new_row, new_col = row + delta_r, col + delta_c
                    if 0 <= new_row < len(array) and 0 <= new_col < len(array[0]) and array[new_row][new_col] == '0':
                        edge = WeightedEdge((row, col), (new_row, new_col), random.randint(1, 6))
                        if edge not in weighted_edges:
                            weighted_edges.append(edge)
    
    return weighted_edges

def find_start(array):
    for i in range (len(array)):
        for j in range (len(array[i])):
            if array[i][j] == 'S':
                return (i,j)
            
def find_goal(array):
    for i in range (len(array)):
        for j in range (len(array[i])):
            if array[i][j] == 'G':
                return (i,j)
            
def calculate_distance(start, goal):
    return abs(start[0] - goal[0]) + (start[1] - goal[1])

def assign_heuristics(array, goal):
    h_array = [['-1' for _ in range(len(array[0]))] for _ in range(len(array))]
    for i in range (len(array)):
        for j in range (len(array[0])):
            h_array[i][j] = calculate_distance((i, j), goal)
    return h_array
    
def sort_array_by_h(frontier, h_array):
    frontier_with_heuristics = [(coord, h_array[coord[0]][coord[1]]) for coord in frontier]
    
    # Sort the list based on the heuristic values
    frontier_with_heuristics.sort(key=lambda x: x[1])
    
    # Extract only the coordinates from the sorted list
    sorted_frontier = [coord[0] for coord in frontier_with_heuristics]
    
    return sorted_frontier

def is_valid(array, row, col, rows, cols, visited):
    if 0 <= row < rows and 0 <= col < cols and array[row][col] != '-1' and not visited[row][col]:
        return True
    return False
           
def create_visited_arr(array):
    visited = [['' for _ in range(len(array[0]))] for _ in range(len(array))]
    return visited

def reconstruct_path(predecessors, end):
    path = [end]
    current = end
    while predecessors[current] is not None:
        current = predecessors[current]
        path.append(current)
    path.reverse()
    return path

def BFS(array): 
    start = find_start(array)
    goal = find_goal(array)
    rows, cols = len(array), len(array[0])
    visited = create_visited_arr(array)
    visited[start[0]][start[1]] = True
    frontier = [start]
    predecessors = {}
    predecessors[start] = None

    while frontier:
        row, col = frontier.pop(0)
        if (row, col) not in visited:
            visited[row][col] = True
        for delta_r, delta_c in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            new_row, new_col = row + delta_r, col + delta_c
            if is_valid(array, new_row, new_col, rows, cols, visited):
                frontier.append((new_row, new_col))
                predecessors[(new_row, new_col)] = (row, col)
                if (new_row, new_col) == goal:
                    return reconstruct_path(predecessors, goal)
    return "Can't find path!"

def DFS(array):
    start = find_start(array)
    goal = find_goal(array)
    rows, cols = len(array), len(array[0])
    visited = create_visited_arr(array)
    visited[start[0]][start[1]] = True
    frontier = [start]
    predecessors = {}
    predecessors[start] = None

    while frontier:
        row, col = frontier.pop()
        if (row, col) not in visited:
            visited[row][col] = True
        for delta_r, delta_c in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            new_row, new_col = row + delta_r, col + delta_c
            if is_valid(array, new_row, new_col, rows, cols, visited):
                frontier.append((new_row, new_col))
                predecessors[(new_row, new_col)] = (row, col)
                if (new_row, new_col) == goal:
                    return reconstruct_path(predecessors, goal)
    return "Can't find path!"
    
def GBFS(array):
    start = find_start(array)
    goal = find_goal(array)
    rows, cols = len(array), len(array[0])
    visited = create_visited_arr(array)
    visited[start[0]][start[1]] = True
    frontier = [start]
    predecessors = {}
    predecessors[start] = None
    h_array = assign_heuristics(array, goal)
    while frontier:
        row, col = frontier.pop(0)
        if (row, col) not in visited:
            visited[row][col] = True
        if (row, col) == goal:
            return reconstruct_path(predecessors, goal)
        for delta_r, delta_c in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            new_row, new_col = row + delta_r, col + delta_c
            if is_valid(array, new_row, new_col, rows, cols, visited):
                frontier.append((new_row, new_col))
                predecessors[(new_row, new_col)] = (row, col)
        frontier = sort_array_by_h(frontier, h_array)
    return "Can't find path!"

def UCS(array):
    start = find_start(array)
    goal = find_goal(array)
    edges = create_random_weight_array(array)
    pq = [(0, start, [])]
    visited = set()
    
    while pq:
        cost, current, path = heapq.heappop(pq)
        
        if current in visited:
            continue
        
        path = path + [current]
        visited.add(current)
        
        if current == goal:
            return path, cost
        
        for edge in edges:
            if edge.vertex1 == current and edge.vertex2 not in visited:
                heapq.heappush(pq, (cost + edge.weight, edge.vertex2, path))
            elif edge.vertex2 == current and edge.vertex1 not in visited:
                heapq.heappush(pq, (cost + edge.weight, edge.vertex1, path))
    return "Doesn't exist a path", None    
def astar(array):
    start = find_start(array)
    goal = find_goal(array)
    edges = create_random_weight_array(array)
    pq = [(0, 0, start, [])]
    visited = set()
    g_costs = {start: 0}
    
    while pq:
        f_cost, cost, current, path = heapq.heappop(pq)
        
        if current in visited:
            continue
        
        path = path + [current]
        visited.add(current)
        
        if current == goal:
            return path, cost
        
        for edge in edges:
            neighbor = None
            if edge.vertex1 == current:
                neighbor = edge.vertex2
            elif edge.vertex2 == current:
                neighbor = edge.vertex1
            
            if neighbor and neighbor not in visited:
                next_g_cost = g_costs[current] + edge.weight
                if neighbor not in g_costs or next_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = next_g_cost
                    f_cost = next_g_cost + calculate_distance(neighbor, goal)
                    heapq.heappush(pq, (f_cost, next_g_cost, neighbor, path))
    
    return "Doesn't exist a path", None
array = [['S', '-1','-1', '0'],
         ['0', '0','0', '0'],
         ['0', '0','0', '0'],
         ['0', '-1','-1', 'G']]
