from typing import List

class ArrayProcessor:
    def __init__(self, arr: List[int]):
        """
        Initialize the ArrayProcessor with an array of integers.
        
        Args:
            arr (List[int]): The input list of integers to process.
        
        Raises:
            ValueError: If input is invalid.
        """
        self.validate_input(arr)
        self.arr = arr

    def validate_input(self, arr: List[int]) -> bool:
        """
        Validate if the input array is a list and contains only integers.
        
        Args:
            arr (List[int]): The input list to validate.
        
        Returns:
            bool: True if valid, False otherwise.

        Raises:
            ValueError: If input is invalid.
        """
        if not isinstance(arr, list):
            raise ValueError("Input must be a list.")
        for item in arr:
            if type(item) is not int:
                raise ValueError("All elements in the list must be integers.")
        return True

    def has_duplicates(self) -> bool:
        """
        Check if there are any duplicate elements in the array.
        
        Returns:
            bool: True if duplicates exist, False otherwise.
        """
        seen = set()
        for item in self.arr:
            if item in seen:
                return True
            seen.add(item)
        return False

# Example usage
if __name__ == "__main__":
    # Valid array
    processor = ArrayProcessor([1, 2, 3, 4])
    
    # Invalid array (contains duplicate and boolean)
    try:
        processor_invalid = ArrayProcessor([5, 5, True])
    except ValueError as e:
        print(e)  # Output: All elements in the list must be integers.