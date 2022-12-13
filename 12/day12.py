import heapq as heap
from collections import defaultdict

INPUT_FILE = '12/input.txt'

def fetch_input():
    results = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n')
            results.append(list(full_line))
    return results

checks = set()
def is_valid_next_pos(current_val, next_val):
    if current_val == 'S' or current_val == 'a':
        valid_next_val = ['S', 'b', 'a']
    elif current_val == 'b':
        valid_next_val = ['S', 'b', 'a', 'c']
    elif current_val == 'E' or current_val == 'z':
        valid_next_val = ['E', 'z', 'y']
    elif current_val == 'y':
        valid_next_val = ['E', 'y', 'z', 'x']
    else:
        valid_next_val = [chr(idx) for idx in range(ord('a'), ord(current_val[0]) + 2)]
    next_vals = ','.join([s for s in valid_next_val])
    checks.add(f'{current_val}:[{next_vals}]')
    return next_val in valid_next_val


def create_key(x, y):
    return f'{x},{y}'


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_key(self):
        return create_key(self.x, self.y)

    def __str__(self):
        return f'[{self.to_key()}]'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class GridMap(object):
    def __init__(self, raw_results):
        self.grid = raw_results
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def get(self, x, y):
        return self.grid[y][x]

    def _find(self, search_val):
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[0])):
                if self.grid[y][x] == search_val:
                    return Point(x, y)

    def find_start_end(self):
        start = self._find('S')
        end = self._find('E')
        return start, end

    def get_adjacents(self, point: Point):
        deltas = [[0, -1], [1, 0], [0, 1], [-1, 0]] # up right down left
        moves = []
        for d in deltas:
            new_x = point.x + d[0]
            new_y = point.y + d[1]

            # Co-Ordinate is valid
            is_valid = (new_x >= 0 and new_y >= 0) and (new_x < self.width and new_y < self.height)

            if is_valid:
                current_pos_val = self.get(point.x, point.y)
                next_val = self.get(new_x, new_y)
                valid_next_pos = is_valid_next_pos(current_pos_val, next_val)
                if valid_next_pos:
                    moves.append(Point(new_x, new_y))
        return moves

    def to_adjacent_list(self):
        adj = defaultdict(list)
        for y in range(0, self.height):
            for x in range(0, self.width):
                k = create_key(x, y)
                adj[k] = [v.to_key() for v in self.get_adjacents(Point(x, y))]
        return adj

    def find_start_positions(self):
        res = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                value = self.get(x, y)
                if value == 'S' or value == 'a':
                    res.append(Point(x, y))
        return res



def shortest_path(graph, source, dest):
    print(f'Shortest path between {source} -> {dest}')
    print(f'Source adjacents: {graph[source]}')
    print(f'Dest adjacents: {graph[dest]}')

    path_list = [[source]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes = {source}
    if source == dest:
        return path_list[0]

    while path_index < len(path_list):
        current_path = path_list[path_index]
        print(current_path)
        last_node = current_path[-1]
        print(last_node)
        next_nodes = graph[last_node]
        # Search goal node
        if dest in next_nodes:
            current_path.append(dest)
            return current_path
        # Add new paths
        for next_node in next_nodes:
            if not next_node in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return []

def dijkstra(G, startingNode):
    visited = set()
    parentsMap = {}
    pq = []
    nodeCosts = defaultdict(lambda: float('inf'))
    nodeCosts[startingNode] = 0
    heap.heappush(pq, (0, startingNode))
    last_node = None
    while pq:
        # go greedily by always extending the shorter cost nodes first
        _, node = heap.heappop(pq)
        visited.add(node)
        last_node = node

        for adjNode in G[node]:
            weight = 1
            if adjNode in visited:	continue

            newCost = nodeCosts[node] + weight
            if nodeCosts[adjNode] > newCost:
                parentsMap[adjNode] = node
                nodeCosts[adjNode] = newCost
                heap.heappush(pq, (newCost, adjNode))

    return parentsMap, nodeCosts, last_node


def part_one():
    raw_results = fetch_input()
    grid = GridMap(raw_results)
    start, end = grid.find_start_end()
    print(f'Travel from {start} to {end} in a grid {grid.width} x {grid.height}')
    adj = grid.to_adjacent_list()
    parentsMap, nodeCosts, last_node = dijkstra(adj, start.to_key())
    print(last_node)
    print(adj[last_node])
    print(nodeCosts[end.to_key()])


def part_two():
    raw_results = fetch_input()
    grid = GridMap(raw_results)
    start, end = grid.find_start_end()
    start_positions = grid.find_start_positions()
    min_steps = 0
    adj = grid.to_adjacent_list()
    paths = []
    for start_item in start_positions:
        parentsMap, nodeCosts, last_node = dijkstra(adj, start_item.to_key())
        paths.append(nodeCosts[end.to_key()])
    print(paths)
    print(min(paths))

if __name__ == "__main__":
    part_two()

