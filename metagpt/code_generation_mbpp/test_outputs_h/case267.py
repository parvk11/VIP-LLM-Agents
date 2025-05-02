## square_sum_function.py

import numpy as np
from typing import List, Union

class square_Sum_function:
    def square_Sum(self, arg0: Union[List[int], np.ndarray]) -> int:
        """
        Calculate the sum of squares for the input list or array.

        Args:
        arg0: List[int] or np.ndarray - Input list or array

        Returns:
        int - Sum of squares
        """
        return int(np.sum(np.square(arg0)))