import os
import random
import string

EXCLUDE_FILES = ['README.md', '.gitignore', 'package.json', 'active_code.py', 'data.txt', 
                'file_operations.py', '.env.template']

def generate_random_filename():
    chars = string.ascii_lowercase + string.digits
    return f"file_{''.join(random.choices(chars, k=6))}.txt"

def create_random_files(num_files=8):
    created_files = []
    for _ in range(num_files):
        filename = generate_random_filename()
        try:
            with open(filename, 'w', newline='\n') as f:
                f.write(f"Random content generated at: {random.randint(1000,9999)}")
            created_files.append(filename)
            print(f"Created: {filename}")
        except Exception as e:
            print(f"Error creating {filename}: {str(e)}")
    return created_files

def delete_random_files(num_files=8):
    all_files = [f for f in os.listdir() 
                if os.path.isfile(f) and f not in EXCLUDE_FILES]
    
    if not all_files:
        print("No files available to delete")
        return []
    
    num_to_delete = min(num_files, len(all_files))
    to_delete = random.sample(all_files, num_to_delete)
    deleted_files = []
    
    for file in to_delete:
        try:
            os.remove(file)
            deleted_files.append(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {str(e)}")
    
    return deleted_files

if __name__ == "__main__":
    num_to_create = random.randint(5, 10)
    num_to_delete = random.randint(5, 10)
    
    print(f"\nCreating {num_to_create} random files...")
    created = create_random_files(num_to_create)
    
    print(f"\nDeleting {num_to_delete} random files...")
    deleted = delete_random_files(num_to_delete)
    
    print(f"\nSummary:")
    print(f"Created {len(created)} files: {', '.join(created)}")
    print(f"Deleted {len(deleted)} files: {', '.join(deleted)}")