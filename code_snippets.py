import random

# List of Python code snippets that can be randomly added or removed
code_snippets = [
    """def calculate_sum(numbers):
    return sum(numbers)""",
    
    """def is_palindrome(text):
    return text == text[::-1]""",
    
    """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)""",
    
    """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr""",
    
    """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1"""
]

def get_random_snippet():
    """Returns a random code snippet from the list"""
    return random.choice(code_snippets)

def get_random_index():
    """Returns a random index from the code snippets list"""
    return random.randint(0, len(code_snippets) - 1)