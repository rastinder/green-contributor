# Active Python Code

def is_palindrome(text):
    return text == text[::-1]

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)