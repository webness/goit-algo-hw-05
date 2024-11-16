def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_limit = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        # Check if mid element is the exact target
        if arr[mid] == target:
            return (iterations, arr[mid])

        # Update the upper limit if current mid is greater than or equal to target
        if arr[mid] >= target:
            upper_limit = arr[mid]
            right = mid - 1
        else:
            left = mid + 1

    # If we exit the loop, upper_limit holds the smallest element >= target, or None if no such element
    return (iterations, upper_limit)


sorted_array = [0.1, 0.5, 0.7, 1.1, 1.5, 2.3, 3.8, 4.4]
target_value = 1.2
result = binary_search(sorted_array, target_value)
print("Iterations:", result[0])
print("Upper limit:", result[1])
