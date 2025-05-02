from minimum_cost_path import MinimumCostPath

def main():
    # Example cost matrix
    cost_matrix = [
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1]
    ]
    m = len(cost_matrix)
    n = len(cost_matrix[0])

    mcp = MinimumCostPath()
    min_cost_path = mcp.min_cost_path(cost_matrix, m, n)
    print(min_cost_path)

if __name__ == "__main__":
    main()
