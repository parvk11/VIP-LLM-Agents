## swap_list_function.py

def swap_List(lst: list, idx1: int, idx2: int) -> None:
    """
    Swaps the elements at the given indices in the input list.

    Args:
    lst: The input list
    idx1: The index of the first element to swap
    idx2: The index of the second element to swap

    Returns:
    None
    """
    if 0 <= idx1 < len(lst) and 0 <= idx2 < len(lst):
        lst[idx1], lst[idx2] = lst[idx2], lst[idx1]