## minimum_cost_path_finder.py

from typing import List, Tuple

class MinimumCostPathFinder:
    def __init__(self, cost_matrix: List[List[int]], dp: List[List[int]]):
        self.cost_matrix = cost_matrix
        self.dp = dp

    def min_cost_path(self, cost_matrix: List[List[int]], m: int, n: int) -> List[Tuple[int, int]]:
        rows = len(cost_matrix)
        cols = len(cost_matrix[0])

        # Initialize the dp matrix with the cost of the starting position
        self.dp[0][0] = cost_matrix[0][0]

        # Fill the first row of the dp matrix
        for i in range(1, cols):
            self.dp[0][i] = self.dp[0][i-1] + cost_matrix[0][i]

        # Fill the first column of the dp matrix
        for i in range(1, rows):
            self.dp[i][0] = self.dp[i-1][0] + cost_matrix[i][0]

        # Fill the rest of the dp matrix
        for i in range(1, rows):
            for j in range(1, cols):
                self.dp[i][j] = cost_matrix[i][j] + min(self.dp[i-1][j], self.dp[i][j-1])

        # Backtrack to find the minimum cost path
        path = []
        x, y = m, n
        while x > 0 and y > 0:
            path.append((x, y))
            if self.dp[x-1][y] < self.dp[x][y-1]:
                x -= 1
            else:
                y -= 1
        while x > 0:
            path.append((x, y))
            x -= 1
        while y > 0:
            path.append((x, y))
            y -= 1
        path.append((0, 0))

        return path[::-1]
