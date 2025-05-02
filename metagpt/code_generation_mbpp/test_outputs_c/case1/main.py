def minCostPath(m, n, cost):
    # Create a DP table of size (m+1) x (n+1)
    dp = [[0 for _ in range(n + 1)] for __ in range(m + 1)]
    
    # Initialize the starting point
    dp[0][0] = cost[0][0]
    
    # Fill the first row
    for i in range(1, n + 1):
        dp[0][i] = dp[0][i - 1] + cost[0][i]
        
    # Fill the first column
    for j in range(1, m + 1):
        dp[j][0] = dp[j - 1][0] + cost[j][0]
    
    # Fill the rest of the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = cost[i][j] + min(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]

# # Example usage
# cost = [
#     [4, 7, 8],
#     [6, 7, 2],
#     [3, 9, 5]
# ]
# m = 2  # rows
# n = 2  # columns
# print("Minimum cost to reach (2,2) is", minCostPath(m, n, cost))
