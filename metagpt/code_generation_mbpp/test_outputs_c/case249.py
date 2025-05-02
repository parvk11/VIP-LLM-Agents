## intersection_array_function.py

from typing import List, Union

def intersection_array(arg0: Union[List[int], List[float], List[str], List[object]],
                       arg1: Union[List[int], List[float], List[str], List[object]],
                       arg2: Union[List[int], List[float], List[str], List[object]],
                       arg3: Union[List[int], List[float], List[str], List[object]],
                       arg4: Union[List[int], List[float], List[str], List[object]],
                       arg5: Union[List[int], List[float], List[str], List[object]],
                       arg6: Union[List[int], List[float], List[str], List[object]],
                       arg7: Union[List[int], List[float], List[str], List[object]],
                       arg8: Union[List[int], List[float], List[str], List[object]],
                       arg9: Union[List[int], List[float], List[str], List[object]],
                       arg10: Union[List[int], List[float], List[str], List[object]],
                       arg11: Union[List[int], List[float], List[str], List[object]],
                       arg12: Union[List[int], List[float], List[str], List[object]]) -> List[object]:
    """
    Find the intersection of multiple arrays.

    Args:
    arg0: List of integers, floats, strings, or objects
    arg1: List of integers, floats, strings, or objects
    arg2: List of integers, floats, strings, or objects
    arg3: List of integers, floats, strings, or objects
    arg4: List of integers, floats, strings, or objects
    arg5: List of integers, floats, strings, or objects
    arg6: List of integers, floats, strings, or objects
    arg7: List of integers, floats, strings, or objects
    arg8: List of integers, floats, strings, or objects
    arg9: List of integers, floats, strings, or objects
    arg10: List of integers, floats, strings, or objects
    arg11: List of integers, floats, strings, or objects
    arg12: List of integers, floats, strings, or objects

    Returns:
    List of common elements among the input arrays
    """
    # Convert input lists to sets for efficient intersection operation
    set0 = set(arg0)
    set1 = set(arg1)
    set2 = set(arg2)
    set3 = set(arg3)
    set4 = set(arg4)
    set5 = set(arg5)
    set6 = set(arg6)
    set7 = set(arg7)
    set8 = set(arg8)
    set9 = set(arg9)
    set10 = set(arg10)
    set11 = set(arg11)
    set12 = set(arg12)

    # Find the intersection of all sets
    intersection = set0.intersection(set1, set2, set3, set4, set5, set6, set7, set8, set9, set10, set11, set12)

    return list(intersection)
