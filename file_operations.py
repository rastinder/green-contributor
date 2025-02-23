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

MIN_FILES_BEFORE_DELETE = 20  # Minimum number of files required before deletion

EXCLUDE_FILES = ['README.md', '.gitignore', 'package.json', 'active_code.py', 
                'data.txt', 'file_operations.py', '.env.template', '.env',
                'TEST_*.py']

CODESTRAL_CONFIG = {
    'api_url': os.getenv('CODESTRAL_API_URL'),
    'model': os.getenv('CODESTRAL_MODEL'),
    'max_tokens': int(os.getenv('CODESTRAL_MAX_TOKENS', 2000)),
    'temperature': float(os.getenv('CODESTRAL_TEMPERATURE', 0.7)),
    'keys': [
        os.getenv('CODESTRAL_API_KEY_1'),
        os.getenv('CODESTRAL_API_KEY_2'),
        os.getenv('CODESTRAL_API_KEY_3')
    ]
}

def count_files_in_workdir() -> int:
    """Count number of files in work directory"""
    try:
        return len([f for f in os.listdir(WORK_DIR) 
                   if os.path.isfile(os.path.join(WORK_DIR, f))])
    except Exception as e:
        print(f"Error counting files: {str(e)}")
        return 0

def generate_random_rating() -> str:
    """Generate a random Norwegian rating"""
    ratings = [
        "Utmerket", "Veldig bra", "Bra", "Grei", "Middels", 
        "Under middels", "Dårlig", "Veldig dårlig"
    ]
    return random.choice(ratings)

def generate_random_review() -> str:
    """Generate a random Norwegian review"""
    adjectives = [
        "interessant", "spennende", "kreativ", "innovativ", "praktisk",
        "effektiv", "nyttig", "smart", "elegant", "solid"
    ]
    nouns = [
        "løsning", "implementasjon", "arkitektur", "design", "kode",
        "struktur", "moduler", "grensesnitt", "funksjonalitet", "system"
    ]
    adverbs = [
        "veldig", "ganske", "utrolig", "særdeles", "bemerkelsesverdig",
        "spesielt", "usedvanlig", "ekstremt", "betydelig", "merkbart"
    ]
    return f"Dette er en {random.choice(adverbs)} {random.choice(adjectives)} {random.choice(nouns)}."

def generate_random_filename() -> str:
    """Generate a random filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chars = string.ascii_lowercase + string.digits
    random_str = ''.join(random.choices(chars, k=6))
    return f"file_{timestamp}_{random_str}.py"

def create_random_files(num_files: int = 8) -> List[str]:
    """Generate Python files in the work directory with Norwegian reviews"""
    created_files = []
    
    for _ in range(num_files):
        filename = os.path.join(WORK_DIR, generate_random_filename())
        try:
            rating = generate_random_rating()
            review = generate_random_review()
            
            content = f'''"""
{review}
Rating: {rating}

Dette er en automatisk generert Python-fil.
"""

import random
from typing import List, Dict, Any
from datetime import datetime

class DataBehandler:
    """Klasse for databehandling"""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.resultat = None
    
    def behandle_data(self) -> None:
        """Behandler input data"""
        self.resultat = {{k: str(v).upper() for k, v in self.data.items()}}
    
    def hent_resultat(self) -> Dict[str, str]:
        """Returnerer behandlet data"""
        return self.resultat if self.resultat else {{}}\n
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
        print(f"\nCreating {num_to_create} Python files with Norwegian reviews...")
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