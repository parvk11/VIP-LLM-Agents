## amicable_numbers_sum_function.py

def sum_of_divisors(n: int) -> int:
    """
    Calculate the sum of divisors of a given number.
    
    Args:
    n: An integer for which the sum of divisors needs to be calculated.
    
    Returns:
    An integer representing the sum of divisors of the given number.
    """
    sum_divisors = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            sum_divisors += i
            if i != n // i:
                sum_divisors += n // i
    return sum_divisors

def amicable_numbers_sum(limit: int) -> int:
    """
    Calculate the sum of amicable numbers within the given range.
    
    Args:
    limit: An integer representing the upper limit of the range within which to find amicable numbers.
    
    Returns:
    An integer representing the sum of amicable numbers within the given range.
    """
    amicable_sum = 0
    for num in range(2, limit):
        sum_div = sum_of_divisors(num)
        if sum_div != num and sum_of_divisors(sum_div) == num:
            amicable_sum += num
    return amicable_sum