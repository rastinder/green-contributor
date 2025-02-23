import os
import logging
from typing import List, Dict, Any
from datetime import datetime
import json
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_processor.log'),
        logging.StreamHandler()
    ]
)

class DataProcessingError(Exception):
    """Custom exception for data processing errors."""
    pass

class DataValidator:
    """Validates input data before processing."""
    
    @staticmethod
    def validate_json(data: str) -> bool:
        """Check if string is valid JSON."""
        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False
    
    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Check if string is valid date format."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

class DataProcessor:
    """Processes and transforms input data."""
    
    def __init__(self, input_data: Dict[str, Any]):
        self.data = input_data
        self.processed = {}
        self.validator = DataValidator()
    
    def normalize_strings(self) -> None:
        """Convert all string values to lowercase and strip whitespace."""
        try:
            for key, value in self.data.items():
                if isinstance(value, str):
                    self.processed[key] = value.lower().strip()
                else:
                    self.processed[key] = value
        except Exception as e:
            logging.error(f"Error normalizing strings: {str(e)}")
            traceback.print_exc()
            raise DataProcessingError("Failed to normalize strings")
    
    def validate_fields(self, required_fields: List[str]) -> bool:
        """Check if all required fields are present."""
        return all(field in self.data for field in required_fields)
    
    def process_dates(self) -> None:
        """Convert date strings to datetime objects."""
        try:
            for key, value in self.data.items():
                if isinstance(value, str) and self.validator.validate_date(value):
                    self.processed[key] = datetime.strptime(value, '%Y-%m-%d')
        except Exception as e:
            logging.error(f"Error processing dates: {str(e)}")
            raise DataProcessingError("Failed to process dates")

def main():
    # Example usage
    sample_data = {
        "name": " John Doe ",
        "date_joined": "2024-02-24",
        "status": "ACTIVE",
        "metadata": "{"role": "user"}"
    }
    
    try:
        processor = DataProcessor(sample_data)
        
        # Validate required fields
        if not processor.validate_fields(['name', 'date_joined']):
            raise DataProcessingError("Missing required fields")
            
        # Process the data
        processor.normalize_strings()
        processor.process_dates()
        
        logging.info("Data processed successfully")
        logging.info(f"Processed data: {processor.processed}")
        
    except DataProcessingError as e:
        logging.error(f"Processing error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
