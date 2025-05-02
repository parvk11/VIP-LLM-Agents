import pytest
from main import minCostPath

def test_minimum_cost_path_example1():
    cost_matrix = [
        [1, 3, 5, 8],
        [4, 2, 1, 7],
        [4, 3, 2, 3]
    ]
    assert minimum_cost_path(cost_matrix) == 13

def test_minimum_cost_path_example2():
    cost_matrix = [
        [1, 2, 3],
        [4, 8, 2],
        [1, 5, 3]
    ]
    assert minimum_cost_path(cost_matrix) == 8

def test_minimum_cost_path_example3():
    cost_matrix = [
        [3, 4, 1, 2],
        [2, 1, 8, 9],
        [4, 7, 8, 1],
        [2, 4, 5, 3]
    ]
    assert minimum_cost_path(cost_matrix) == 15
