
# test_find_largest_integers.py

from find_largest_integers import FindLargestIntegers

def test_find_largest_integers():
    numbers = [4, 7, 2, 9, 5, 1, 8, 6, 3]
    assert FindLargestIntegers.find_largest_integers(numbers) == [9, 8, 7]

def test_find_largest_integers_empty_list():
    numbers = []
    assert FindLargestIntegers.find_largest_integers(numbers) == []

def test_find_largest_integers_duplicate_values():
    numbers = [5, 5, 5, 5, 5]
    assert FindLargestIntegers.find_largest_integers(numbers) == [5, 5, 5]
