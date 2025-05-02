## second_smallest_function.py

def second_smallest(arg0, arg1, arg2, arg3, arg4, arg5):
    """
    Find the second smallest number in a list of 6 numbers.

    Args:
    arg0, arg1, arg2, arg3, arg4, arg5: int - The 6 numbers to be evaluated.

    Returns:
    int - The second smallest number in the list.
    """
    numbers = [arg0, arg1, arg2, arg3, arg4, arg5]
    numbers.sort()
    return numbers[1]
