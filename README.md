# File Operations Plan

## Objective
Create and delete random files programmatically through a Python script.

## Implementation Steps

1. Create `file_operations.py` with:
```python
import os
import random
import string

EXCLUDE_FILES = ['README.md', '.gitignore', 'package.json', 'active_code.py', 'data.txt']

def generate_random_filename():
    chars = string.ascii_lowercase + string.digits
    return f"file_{''.join(random.choices(chars, k=6))}.txt"

def create_random_files(num_files=8):
    for _ in range(num_files):
        filename = generate_random_filename()
        with open(filename, 'w') as f:
            f.write(f"Random content: {random.randint(1000,9999)}")

def delete_random_files(num_files=8):
    all_files = [f for f in os.listdir()
                if os.path.isfile(f) and f not in EXCLUDE_FILES]
    
    if not all_files:
        print("No files available to delete")
        return
    
    to_delete = random.sample(all_files, min(num_files, len(all_files)))
    for file in to_delete:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {str(e)}")

if __name__ == "__main__":
    create_random_files(random.randint(5, 10))
    delete_random_files(random.randint(5, 10))
    print("File operations completed")
```
2. Execute with: `python file_operations.py`

## Required Mode Switch
Switch to Code mode to implement and execute this solution
# Green Contributor

This tool automates GitHub contributions by making random commits throughout the day.

## Setup

1. Create a new private GitHub repository
2. Clone it to your local machine
3. Copy these files into the repository
4. Configure the .env file:
   - Set your GitHub token in GITHUB_TOKEN
   - Set your GitHub username in GITHUB_USERNAME
5. Install dependencies:
```bash
npm install
```
5. Initialize git and set remote:
```bash
git init
git remote add origin YOUR_REPO_URL
git branch -M main
```
6. Make initial commit:
```bash
git add .
git commit -m "Initial commit"
git push -u origin main
```
7. Run the tool:
```bash
npm start
```

## Running as a Background Process (Windows)

1. Install pm2 globally:
```bash
npm install -g pm2
```

2. Start the process:
```bash
pm2 start index.js
```

3. Make it start on boot:
```bash
pm2 startup
pm2 save
```

4. To check status:
```bash
pm2 status
```

Note: This tool is for educational purposes only. Use responsibly.