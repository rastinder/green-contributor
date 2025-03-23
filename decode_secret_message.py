import requests
from bs4 import BeautifulSoup
import re

def decode_secret_message(url):
    """
    Decodes a secret message from a Google Doc containing Unicode characters and their positions.
    
    Args:
        url (str): URL of the Google Doc containing the character data
        
    Returns:
        None: Prints the grid of characters that forms the secret message
    """
    # Fetch the document content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching document: {response.status_code}")
        return
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the text content from the document
    # Google Docs typically have content in div elements with class 'kix-paragraphrenderer'
    content = soup.get_text()
    
    # Parse the coordinates and characters
    # Expected format: character (x, y)
    pattern = r'([^\s\(]+)\s*\((\d+),\s*(\d+)\)'
    matches = re.findall(pattern, content)
    
    if not matches:
        print("No character data found in the document.")
        return
    
    # Extract coordinates and characters
    grid_data = []
    max_x = 0
    max_y = 0
    
    for match in matches:
        char, x_str, y_str = match
        x, y = int(x_str), int(y_str)
        grid_data.append((char, x, y))
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    
    # Create the grid (adding 1 because coordinates are 0-indexed)
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    # Fill the grid with characters
    for char, x, y in grid_data:
        grid[y][x] = char
    
    # Print the grid
    for row in grid:
        print(''.join(row))

# Example usage
if __name__ == "__main__":
    # Example Google Doc URL
    example_url = "https://docs.google.com/document/d/1yx0SE-S3m1VvY-B6RRSuY8ybW8WoG3YRTFpM9Eby3Sk/edit"
    
    print("Decoding secret message from Google Doc...")
    decode_secret_message(example_url)
    print("\nNote: Make sure to view the output in a fixed-width font to see the secret message correctly.")