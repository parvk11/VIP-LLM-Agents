


# assert min_cost([[2, 3, 4], [5, 9, 3], [2, 6, 4]], 2, 2) == 12
# assert min_cost([[3, 4, 5], [6, 10, 4], [3, 7, 5]], 2, 2) == 16
# assert min_cost([[2, 3, 4], [5, 9, 3], [2, 6, 4]], 2, 2) == 12
# assert min_cost([[3, 4, 5], [6, 10, 4], [3, 7, 5]], 2, 2) == 16

from cost_matrix import MinimumCostPath

def test_min_cost_path():

    # Test case 1: Basic test case
    cost_matrix = [[2, 3, 4], [5, 9, 3], [2, 6, 4]]
    target_x = 3
    target_y = 3
    path_finder = MinimumCostPath()
    print(path_finder.min_cost_path(cost_matrix, target_x, target_y) == 12)
    print(path_finder.min_cost_path(cost_matrix, target_x, target_y))

    # Test case 2: Another basic test case
    cost_matrix = [[3, 4, 5], [6, 10, 4], [3, 7, 5]]
    target_x = 2
    target_y = 2
    path_finder = MinimumCostPath()
    print(path_finder.min_cost_path(cost_matrix, target_x, target_y) == 16)
    print(path_finder.min_cost_path(cost_matrix, target_x, target_y))

    # Test case 3:: Another basic test case
    cost_matrix = [[2, 3,4], [5, 9, 3], [2, 6, 4]]
    target_x = 2
    target_y = 2
    path_finder = MinimumCostPath()
    print(path_finder.min_cost_path(cost_matrix, target_x, target_y) == 12)
    print(path_finder.min_cost_path(cost_matrix, target_x, target_y))
    

    
    # Test case 4: Another basic test case
    cost_matrix = [[3, 4, 5], [6, 10, 4], [3, 7, 5]]
    target_x = 2
    target_y = 2
    path_finder = MinimumCostPath()
    print(path_finder.min_cost_path(cost_matrix, target_x, target_y) == 16)
    print(path_finder.min_cost_path(cost_matrix, target_x, target_y))

test_min_cost_path()
