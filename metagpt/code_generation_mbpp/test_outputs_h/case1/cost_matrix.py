## minimum_cost_path.py

class MinimumCostPath:
    def __init__(self):
        self.cost_matrix = []
        self.visited = set()
        self.min_cost = {}
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def min_cost_path(self, cost_matrix: list, m: int, n: int) -> list:
        if not cost_matrix or m <= 0 or n <= 0:
            return []

        self.cost_matrix = cost_matrix
        self.min_cost = {(i, j): float('inf') for i in range(m) for j in range(n)}
        self.min_cost[(0, 0)] = self.cost_matrix[0][0]

        queue = [(0, 0)]

        while queue:
            x, y = queue.pop(0)
            self.visited.add((x, y))

            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in self.visited:
                    new_cost = self.min_cost[(x, y)] + self.cost_matrix[nx][ny]
                    if new_cost < self.min_cost[(nx, ny)]:
                        self.min_cost[(nx, ny)] = new_cost
                        queue.append((nx, ny))

        path = []
        x, y = m - 1, n - 1
        while (x, y) != (0, 0):
            path.append((x, y))
            min_nei = min((nx, ny) for nx, ny in self.visited if nx == x and ny == y)
            x, y = min_nei
        path.append((0, 0))
        return path[::-1]
