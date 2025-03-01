import os
import random
import requests
import string
from typing import List, Tuple
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a dedicated directory for file operations
WORK_DIR = "generated_files"
if not os.path.exists(WORK_DIR):
    os.makedirs(WORK_DIR)

MIN_FILES_BEFORE_DELETE = 10  # Minimum number of files required before deletion

EXCLUDE_FILES = ['README.md', '.gitignore', 'package.json', 'active_code.py',
                'data.txt', 'file_operations.py', '.env.template', '.env',
                'TEST_*.py', '*.txt', 'run_silent.vbs', 'token_instructions.md']

CODESTRAL_CONFIG = {
    'api_url': os.getenv('CODESTRAL_API_URL'),
    'model': os.getenv('CODESTRAL_MODEL'),
    'max_tokens': int(os.getenv('CODESTRAL_MAX_TOKENS', 2000)),
    'temperature': float(os.getenv('CODESTRAL_TEMPERATURE', 0.7)),
    'keys': [
        os.getenv('CODESTRAL_API_KEY_1'),
        os.getenv('CODESTRAL_API_KEY_2'),
        os.getenv('CODESTRAL_API_KEY_3')
    ],
    'rps': int(os.getenv('CODESTRAL_RPS', 1))
}

def generate_fallback_code() -> str:
    """Generate fallback code when API fails"""
    snippets = [
        '''def process_data(data: dict) -> dict:
    """Process input data with validation and transformation"""
    try:
        return {k.upper(): str(v).lower() for k, v in data.items()}
    except Exception as e:
        return {"error": str(e)}''',
        
        '''def analyze_text(text: str) -> dict:
    """Analyze text and return statistics"""
    return {
        "length": len(text),
        "words": len(text.split()),
        "uppercase": sum(1 for c in text if c.isupper()),
        "lowercase": sum(1 for c in text if c.islower())
    }''',
        
        '''def transform_list(items: list) -> list:
    """Transform list items with type checking"""
    try:
        return [str(item).capitalize() for item in items]
    except Exception as e:
        return [str(e)]'''
    ]
    return random.choice(snippets)

def count_files_in_workdir() -> int:
    """Count number of files in work directory"""
    try:
        return len([f for f in os.listdir(WORK_DIR) 
                   if os.path.isfile(os.path.join(WORK_DIR, f))])
    except Exception as e:
        print(f"Error counting files: {str(e)}")
        return 0

def generate_code_with_llm() -> str:
    """Generate Python code using Codestral API with fallback"""
    if not any(CODESTRAL_CONFIG['keys']):
        return generate_fallback_code()

    prompt = """Write a Python function that does data processing or analysis. Include:
    - Type hints
    - Docstring
    - Error handling
    - Clear, commented code
    Make it a single function that's useful and well-documented."""
    
    headers = {
        'Authorization': f'Bearer {random.choice(CODESTRAL_CONFIG["keys"])}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': CODESTRAL_CONFIG['model'],
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': CODESTRAL_CONFIG['max_tokens'],
        'temperature': CODESTRAL_CONFIG['temperature']
    }
    from openai import OpenAI
    import openai

    try:
        # Initialize OpenAI client with retries
        client = OpenAI(
            api_key=random.choice(CODESTRAL_CONFIG['keys']),
            base_url=CODESTRAL_CONFIG['api_url'],
            max_retries=2,
            timeout=10.0
        )

        messages = [{"role": "user", "content": prompt}]
        
        try:
            response = client.chat.completions.create(
                model=CODESTRAL_CONFIG['model'],
                messages=messages,
                temperature=CODESTRAL_CONFIG['temperature'],
                max_tokens=CODESTRAL_CONFIG['max_tokens'],
                stream=False
            )
            content = response.choices[0].message.content
            
            # Extract code from response if needed
            if '```python' in content:
                code = content.split('```python')[1].split('```')[0].strip()
            else:
                code = content.strip()
                
            if not code or "# Error" in code or "# Failed" in code:
                print("Invalid or empty response from API, using fallback")
                return generate_fallback_code()
            return code
            
        except openai.APITimeoutError:
            print("API timeout, using fallback")
            return generate_fallback_code()
        except openai.RateLimitError:
            print("Rate limit exceeded, using fallback")
            return generate_fallback_code()
        except openai.APIError as e:
            print(f"API error: {str(e)}, using fallback")
            return generate_fallback_code()
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}, using fallback")
        return generate_fallback_code()



def generate_random_filename() -> str:
    """Generate a random filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chars = string.ascii_lowercase + string.digits
    random_str = ''.join(random.choices(chars, k=6))
    return f"file_{timestamp}_{random_str}.py"

def create_random_files(num_files: int = 8) -> List[str]:
    """Generate Python files in the work directory with LLM-generated code"""
    created_files = []
    
    for _ in range(num_files):
        filename = os.path.join(WORK_DIR, generate_random_filename())
        try:
            generated_code = generate_code_with_llm()
            if "# Error" in generated_code or "# Failed" in generated_code:
                print("Using fallback code instead")
                generated_code = generate_fallback_code()
            
            # Add necessary imports based on the code type
            imports = """from typing import Dict, List, Any, Union
import json
from datetime import datetime
from inspect import getmembers, isfunction
import csv
import os

"""
            
            content = f'''"""
Auto-generated Python file for GitHub contributions.
Generated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

This file contains Python code for data processing with error handling.
"""

{imports}

{generated_code}

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
                {{"name": "Test User", "age": 25, "status": "ACTIVE"}},
                {{"input": "Hello", "value": 123, "type": "test"}}
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
            print("\\nRunning tests...")
            for i, data in enumerate(test_data, 1):
                try:
                    print(f"\\nTest #{i}")
                    if isinstance(data, tuple):
                        print(f"Input: {{data}}")
                        result = func(*data)
                    else:
                        print(f"Input: {{json.dumps(data, indent=2)}}")
                        result = func(data)
                    print(f"Result: {{json.dumps(result, default=str, indent=2)}}")
                except Exception as e:
                    print(f"Error: {{str(e)}}")
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
    for util_func in ['run_tests', 'getmembers', 'isfunction']:
        all_functions.pop(util_func, None)
    
    # Now run the tests with the available functions
    run_tests()
'''
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            created_files.append(filename)
            print(f"Created: {filename}")
            
        except Exception as e:
            print(f"Error creating {filename}: {str(e)}")
    
    return created_files

def delete_random_files(num_files: int = 8) -> Tuple[List[str], bool]:
    """Delete random files from work directory only if min files requirement is met"""
    current_file_count = count_files_in_workdir()
    
    if current_file_count < MIN_FILES_BEFORE_DELETE:
        print(f"Not enough files to delete. Current count: {current_file_count}, Required: {MIN_FILES_BEFORE_DELETE}")
        return [], False
        
    try:
        all_files = [f for f in os.listdir(WORK_DIR) 
                    if os.path.isfile(os.path.join(WORK_DIR, f))]
        
        num_to_delete = min(num_files, len(all_files))
        to_delete = random.sample(all_files, num_to_delete)
        deleted_files = []
        
        for file in to_delete:
            try:
                file_path = os.path.join(WORK_DIR, file)
                os.remove(file_path)
                deleted_files.append(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {str(e)}")
        
        return deleted_files, True
    except Exception as e:
        print(f"Error in delete_random_files: {str(e)}")
        return [], False

if __name__ == "__main__":
    print(f"\nWorking Directory: {WORK_DIR}")
    current_files = count_files_in_workdir()
    
    print(f"Current file count: {current_files}")
    if current_files < MIN_FILES_BEFORE_DELETE:
        num_to_create = MIN_FILES_BEFORE_DELETE - current_files + random.randint(0, 5)
        print(f"\nCreating {num_to_create} Python files with LLM-generated code...")
        created = create_random_files(num_to_create)
        
        print(f"\nNew file count: {count_files_in_workdir()}")
        print(f"Created {len(created)} files: {', '.join(os.path.basename(f) for f in created)}")
    else:
        num_to_delete = random.randint(1, 5)
        print(f"\nAttempting to delete {num_to_delete} files...")
        deleted, success = delete_random_files(num_to_delete)
        
        if success:
            print(f"\nDeleted {len(deleted)} files: {', '.join(deleted)}")
            print(f"Remaining files: {count_files_in_workdir()}")
        else:
            print("No files were deleted")