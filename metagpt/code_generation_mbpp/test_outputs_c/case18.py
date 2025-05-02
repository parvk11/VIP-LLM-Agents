## Code
def remove_dirty_chars(data, dirty_chars):
    """
    Removes dirty characters from the input data.

    Args:
    data: Union[str, list, dict]. The input data from which dirty characters are to be removed.
    dirty_chars: str. The dirty characters to be removed from the input data.

    Returns:
    str. The cleaned data after removing the dirty characters.
    """
    if isinstance(data, str):
        cleaned_data = data.translate(str.maketrans('', '', dirty_chars))
    elif isinstance(data, list):
        cleaned_data = [item.translate(str.maketrans('', '', dirty_chars)) for item in data]
    elif isinstance(data, dict):
        cleaned_data = {key: value.translate(str.maketrans('', '', dirty_chars)) for key, value in data.items()}
    else:
        raise ValueError("Input data type not supported. Supported types: str, list, dict")

    return cleaned_data
