## eulerian_number_function.py

import sympy

class EulerianNumberFunction:
    def eulerian_num(self, n: int, m: int) -> int:
        """
        Calculate the Eulerian number A(n, m) using sympy library.

        Args:
        n: An integer representing the row index.
        m: An integer representing the column index.

        Returns:
        An integer representing the Eulerian number A(n, m).
        """
        return int(sympy.functions.combinatorial.numbers.euler(n, m))