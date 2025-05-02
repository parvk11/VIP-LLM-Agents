import heapq

class MaxHeap:
    def find_largest_numbers(self, nums: list[int], k: int = 1) -> list[int]:
        """
        Find the k largest numbers in a given list using heapq.nlargest() for optimal performance.
        
        Args:
            nums (list[int]): A list of integers.
            k (int): The number of largest elements to find. Defaults to 1.
            
        Returns:
            list[int]: A list containing the k largest integers from the input list.
        """
        return heapq.nlargest(k, nums)
