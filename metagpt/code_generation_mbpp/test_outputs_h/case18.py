## remove_dirty_chars_function.py

from typing import Union

def remove_dirty_chars(arg0: Union[str, list, dict], arg1: str) -> Union[str, list, dict]:
    """
    Removes dirty characters from the input data.
    Args:
        arg0 (Union[str, list, dict]): The input data.
        arg1 (str): The dirty characters to be removed.
    Returns:
        Union[str, list, dict]: The cleaned data.
    Raises:
        ValueError: If the input data type is not supported.
        TypeError: If the input data is not valid.
    """
    if isinstance(arg0, str):
        return arg0.translate({ord(c): None for c in arg1})
    elif isinstance(arg0, list):
        return [item.translate({ord(c): None for c in arg1}) for item in arg0]
    elif isinstance(arg0, dict):
        return {key: value.translate({ord(c): None for c in arg1}) for key, value in arg0.items()}
    else:
        raise ValueError("Unsupported data type: {}".format(type(arg0).__name__))