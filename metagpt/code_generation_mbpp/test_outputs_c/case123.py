## amicable_numbers_sum_function.py

"""
This module provides a function to efficiently calculate the sum of amicable numbers and handle large numbers, along with clear documentation for easy integration.
"""

def sum_of_divisors(n):
    """
    Returns the sum of proper divisors of a given number n.
    """
    sum_divisors = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            sum_divisors += i
            if i != n // i:
                sum_divisors += n // i
    return sum_divisors

def amicable_numbers_sum(limit):
    """
    Returns the sum of all amicable numbers below the given limit.

    Args:
    limit: An integer specifying the upper limit for finding amicable numbers.

    Returns:
    An integer representing the sum of all amicable numbers below the given limit.
    """
    amicable_sum = 0
    for num in range(2, limit):
        sum_num = sum_of_divisors(num)
        if sum_num > num and sum_of_divisors(sum_num) == num:
            amicable_sum += num + sum_num
    return amicable_sum
