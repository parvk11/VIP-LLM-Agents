## count_reverse_pairs_function.py

def count_reverse_pairs(arr, left, right, temp, temp_index):
    """
    Count the number of reverse pairs in the given input array using the merge sort algorithm.

    Args:
    arr: List[int], the input array
    left: int, the left index of the subarray
    right: int, the right index of the subarray
    temp: List[int], the temporary array for merging
    temp_index: List[int], the temporary array for index tracking

    Returns:
    int, the number of reverse pairs in the array
    """

    if left >= right:
        return 0

    mid = (left + right) // 2
    count = count_reverse_pairs(arr, left, mid, temp, temp_index) + count_reverse_pairs(arr, mid + 1, right, temp, temp_index)

    i, j, k = left, mid + 1, left
    while i <= mid and j <= right:
        if arr[i] > arr[j]:
            count += mid - i + 1
            temp[k] = arr[j]
            temp_index[k] = j
            j += 1
        else:
            temp[k] = arr[i]
            temp_index[k] = i
            i += 1
        k += 1

    while i <= mid:
        temp[k] = arr[i]
        temp_index[k] = i
        i += 1
        k += 1

    while j <= right:
        temp[k] = arr[j]
        temp_index[k] = j
        j += 1
        k += 1

    for i in range(left, right + 1):
        arr[i] = temp[i]
        temp_index[i] = temp_index[i]

    return count