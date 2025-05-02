## square_sum_function.py

import numpy as np
from typing import Union, List

def square_Sum(arg0: Union[int, float, List[Union[int, float]]]) -> Union[int, float]:
    """
    Calculate the sum of squares for the given input.

    Args:
    arg0: Union[int, float, List[Union[int, float]]] - The input number or list of numbers

    Returns:
    Union[int, float] - The sum of squares of the input numbers
    """
    if isinstance(arg0, (int, float)):
        return arg0**2
    elif isinstance(arg0, list):
        return np.sum(np.array(arg0)**2)
    else:
        raise ValueError("Invalid input type. Please provide an integer, float, or a list of integers/floats.")
