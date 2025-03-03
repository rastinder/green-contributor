"""
Auto-generated Python file for GitHub contributions.
Generated at: 2025-03-03 22:00:11

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

def analyze_data(df: pd.DataFrame) -> Dict[str, Union[float, int, Dict[str, int]]]:
    """
    Analyze a pandas DataFrame by calculating the mean, median, and standard deviation
    for numerical columns and counting the occurrences of unique values for categorical columns.

    Parameters:
    df (pd.DataFrame): The input DataFrame to analyze.

    Returns:
    Dict[str, Union[float, int, Dict[str, int]]]: A dictionary containing the analysis results.
    The keys are column names and the values are dictionaries with 'mean', 'median', 'std', or 'value_counts'.

    Raises:
    ValueError: If the input is not a pandas DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    analysis_results = {}

    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            # Numerical column analysis
            analysis_results[column] = {
                'mean': df[column].mean(),
                'median': df[column].median(),
                'std': df[column].std()
            }
        elif pd.api.types.is_categorical_dtype(df[column]) or df[column].dtype == 'object':
            # Categorical column analysis
            value_counts = df[column].value_counts().to_dict()
            analysis_results[column] = {
                'value_counts': value_counts
            }
        else:
            # Skip columns that are neither numerical nor categorical
            continue

    return analysis_results

# Example usage:
# df = pd.DataFrame({
#     'numeric_col': [1, 2, 3, 4, 5],
#     'categorical_col': ['A', 'B', 'A', 'C', 'B']
# })
# result = analyze_data(df)
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
