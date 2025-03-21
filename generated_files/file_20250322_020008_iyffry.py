"""
Auto-generated Python file for GitHub contributions.
Generated at: 2025-03-22 02:00:12

This file contains Python code for data processing with error handling.
"""

from typing import Dict, List, Any, Union
import json
from datetime import datetime
from inspect import getmembers, isfunction, currentframe
import csv
import os
import pandas as pd



import pandas as pd
from typing import Dict, Union

def analyze_data(df: pd.DataFrame) -> Dict[str, Union[float, Dict[str, float]]]:
    """
    Analyze a pandas DataFrame by calculating the mean, median, and standard deviation for each numerical column.

    Parameters:
    df (pd.DataFrame): The input DataFrame to analyze.

    Returns:
    Dict[str, Union[float, Dict[str, float]]]: A dictionary containing the overall mean, median, and standard deviation
                                                of all numerical columns, and a nested dictionary with these statistics
                                                for each numerical column.

    Raises:
    ValueError: If the input DataFrame is empty or contains no numerical columns.
    """
    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("The input DataFrame is empty.")

    # Select only numerical columns
    numerical_cols = df.select_dtypes(include=['number'])

    # Check if there are any numerical columns
    if numerical_cols.empty:
        raise ValueError("The input DataFrame contains no numerical columns.")

    # Calculate overall statistics
    overall_mean = numerical_cols.mean().mean()
    overall_median = numerical_cols.median().median()
    overall_std = numerical_cols.std().mean()

    # Calculate statistics for each numerical column
    column_stats = {}
    for col in numerical_cols.columns:
        column_stats[col] = {
            'mean': numerical_cols[col].mean(),
            'median': numerical_cols[col].median(),
            'std': numerical_cols[col].std()
        }

    # Combine overall and column-specific statistics
    result = {
        'overall_mean': overall_mean,
        'overall_median': overall_median,
        'overall_std': overall_std,
        'column_stats': column_stats
    }

    return result

# Example usage:
# df = pd.DataFrame({
#     'A': [1, 2, 3, 4, 5],
#     'B': [5, 6, 7, 8, 9],
#     'C': ['a', 'b', 'c', 'd', 'e']
# })
# print(analyze_data(df))

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
