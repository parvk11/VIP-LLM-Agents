from array_dup import ArrayProcessor

 # Test cases
    # "assert test_duplicate(([1,2,3,4,5]))==False", "assert test_duplicate(([1,2,3,4, 4]))==True", "assert test_duplicate([1,1,2,2,3,3,4,4,5])==True"]

processor = ArrayProcessor([1, 2, 3, 4, 5])
if processor.has_duplicates() != False:
    raise AssertionError("Test case failed for input [1, 2, 3, 4, 5]")

processor = ArrayProcessor([1, 2, 3, 4, 4])
if processor.has_duplicates() != True:
    raise AssertionError("Test case failed for input [1, 2, 3, 4, 4]")

processor = ArrayProcessor([1, 1, 2, 2, 3, 3, 4, 4, 5])
if processor.has_duplicates() != True:
    raise AssertionError("Test case failed for input [1, 1, 2, 2, 3, 3, 4, 4, 5]")

processor = ArrayProcessor([1, 2, 3, 4, 5, 6])
if processor.has_duplicates() != False:
    raise AssertionError("Test case failed for input [1, 2, 3, 4, 5, 6]")