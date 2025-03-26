"""
Auto-generated Python file for GitHub contributions.
Generated at: 2025-03-26 06:30:30

This file contains Python code for data processing with error handling.
"""

from typing import Dict, List, Any, Union
import json
from datetime import datetime
from inspect import getmembers, isfunction, currentframe
import csv
import os
import pandas as pd



import csv
from typing import List, Dict, Tuple, Union
import statistics

def process_csv(file_path: str) -> Union[Dict[str, Tuple[float, float]], str]:
    """
    Processes a CSV file to calculate the mean and standard deviation for each column.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Union[Dict[str, Tuple[float, float]], str]: A dictionary where keys are column names and values are tuples
        containing the mean and standard deviation of the column. If an error occurs, returns an error message.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the file is not a valid CSV or contains non-numeric data.
    """
    try:
        # Open the CSV file
        with open(file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            # Initialize a dictionary to store the results
            results: Dict[str, Tuple[float, float]] = {}

            # Iterate over each row in the CSV file
            for row in reader:
                for key, value in row.items():
                    # Convert the value to a float
                    try:
                        float_value = float(value)
                    except ValueError:
                        return f"Error: Non-numeric data found in column '{key}'."

                    # Initialize the list for the column if it doesn't exist
                    if key not in results:
                        results[key] = ([], [])

                    # Append the value to the list for the column
                    results[key][0].append(float_value)

            # Calculate the mean and standard deviation for each column
            for key in results:
                mean = statistics.mean(results[key][0])
                std_dev = statistics.stdev(results[key][0]) if len(results[key][0]) > 1 else 0.0
                results[key] = (mean, std_dev)

            return results

    except FileNotFoundError:
        return f"Error: The file '{file_path}' does not exist."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Example usage:
# result = process_csv('data.csv')
# print(result)

def run_tests():
    """Execute tests based on the function type"""
    funcs = dict(getmembers(globals(), isfunction))
    test_data = None
    func = None

    # Create a temporary test file for CSV functions if needed
    test_csv = None
    if any(name for name in funcs if 'csv' in name.lower()):
        test_csv = 'test_data.csv'
        with open(test_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'age', 'salary'])
            writer.writerow(['John', '30', '50000'])
            writer.writerow(['Alice', '25', '45000'])
    
    try:
        if 'process_data' in funcs:
            test_data = [
                {"name": "Test User", "age": 25, "status": "ACTIVE"},
                {"input": "Hello", "value": 123, "type": "test"}
            ]
            func = process_data
        elif 'analyze_text' in funcs:
            test_data = [
                "Hello World! This is a Test String.",
                "UPPER lower 12345 !@#$%"
            ]
            func = analyze_text
        elif 'transform_list' in funcs:
            test_data = [
                ["item1", "ITEM2", "Item3"],
                ["Python", "JAVA", "TypeScript"]
            ]
            func = transform_list
        elif 'process_csv' in funcs:
            test_data = [
                ('test_data.csv', 'age'),
                ('test_data.csv', 'salary')
            ]
            func = process_csv
        elif 'calculate_average_from_csv' in funcs:
            test_data = [
                ('test_data.csv', 'age'),
                ('test_data.csv', 'salary')
            ]
            func = calculate_average_from_csv
        elif 'process_and_analyze_data' in funcs:
            test_data = [
                ('test_data.csv', 'age'),
                ('test_data.csv', 'salary')
            ]
            func = process_and_analyze_data
        
        if func and test_data:
            print("\nRunning tests...")
            for test_index, data in enumerate(test_data, 1):
                try:
                    print(f"\nTest #{test_index}")
                    if isinstance(data, tuple):
                        print(f"Input: {data}")
                        result = func(*data)
                    else:
                        print(f"Input: {json.dumps(data, indent=2)}")
                        result = func(data)
                    # Improved JSON serialization with better handling of various data types
                    def json_serializer(obj):
                        if isinstance(obj, (datetime, pd.Timestamp)):
                            return obj.isoformat()
                        elif isinstance(obj, (tuple, set)):
                            return list(obj)
                        elif hasattr(obj, '__dict__'):
                            return obj.__dict__
                        return str(obj)
                    
                    print(f"Result: {json.dumps(result, default=json_serializer, indent=2)}")
                except Exception as e:
                    print(f"Error: {str(e)}")
        else:
            print("No suitable test function found")
    
    finally:
        # Clean up test file if it was created
        if test_csv and os.path.exists(test_csv):
            os.remove(test_csv)

if __name__ == "__main__":
    # Get all functions in the current module
    all_functions = dict(getmembers(globals(), isfunction))
    # Remove utility functions to avoid confusion
    for util_func in ['run_tests', 'getmembers', 'isfunction', 'currentframe']:
        all_functions.pop(util_func, None)
    
    # Define generated_code variable to avoid reference errors
    generated_code = ''
    for func_name in all_functions:
        generated_code += func_name + ' '
        
    # Now run the tests with the available functions
    run_tests()
