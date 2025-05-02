## second_smallest_function.py

def second_smallest(arg0: int, arg1: int, arg2: int, arg3: int, arg4: int, arg5: int) -> int:
    """
    Find the second smallest number in a list of 6 numbers.

    Args:
    arg0: int : First number
    arg1: int : Second number
    arg2: int : Third number
    arg3: int : Fourth number
    arg4: int : Fifth number
    arg5: int : Sixth number

    Returns:
    int : Second smallest number
    """
    numbers = [arg0, arg1, arg2, arg3, arg4, arg5]
    numbers.sort()
    return numbers[1]