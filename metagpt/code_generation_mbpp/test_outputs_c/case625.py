## swap_list_function.py

def swap_List(lst, idx1, idx2):
    """
    Swaps the elements at the given indices in the input list.

    Args:
    lst: list - The input list
    idx1: int - The index of the first element to swap
    idx2: int - The index of the second element to swap

    Returns:
    list - The input list with the elements at idx1 and idx2 swapped
    """
    if not isinstance(lst, list):
        raise TypeError("Input must be a list")
    if not isinstance(idx1, int) or not isinstance(idx2, int):
        raise TypeError("Indices must be integers")

    if idx1 < 0 or idx1 >= len(lst) or idx2 < 0 or idx2 >= len(lst):
        raise IndexError("Index out of range")

    lst[idx1], lst[idx2] = lst[idx2], lst[idx1]
    return lst
