## eulerian_number_function.py

def eulerian_num(n, m):
    """
    Calculate the Eulerian number A(n, m) using the given parameters.

    Args:
    n: An integer representing the first parameter of the Eulerian number.
    m: An integer representing the second parameter of the Eulerian number.

    Returns:
    An integer representing the calculated Eulerian number A(n, m).
    """
    if m == 0:
        if n == 0:
            return 1
        else:
            return 0
    elif m == 1:
        if n == 0:
            return 0
        else:
            return 1
    else:
        return (n - m) * eulerian_num(n - 1, m) + (m + 1) * eulerian_num(n - 1, m - 1)

