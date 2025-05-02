## Code
def even_bit_set_number(arg0: int) -> bool:
    """
    Check if the number has even bit set.

    Args:
    arg0: int - The number to be checked.

    Returns:
    bool - True if the number has even bit set, False otherwise.
    """
    # Using bitwise AND to check if the number has even bit set
    return bin(arg0).count('1') % 2 == 0
