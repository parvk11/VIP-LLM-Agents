## even_bit_set_number_function.py

def even_bit_set_number(arg0: int) -> bool:
    """
    Check if the number has even bit set using bitwise operators.

    Args:
    arg0: int - The number to be checked

    Returns:
    bool - True if the number has even bit set, False otherwise
    """
    return (arg0 & 1) == 0