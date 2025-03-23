import requests
import re

def decode_secret_message(url):
    # Extract the document ID from the Google Docs URL
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if not match:
        raise ValueError("Invalid Google Doc URL format")
    doc_id = match.group(1)
    export_url = f'https://docs.google.com/document/d/{doc_id}/export?format=txt'
    
    # Fetch the document content
    response = requests.get(export_url)
    response.raise_for_status()  # Ensure the request was successful
    
    # Decode the content handling UTF-8 BOM
    content = response.content.decode('utf-8-sig')
    
    # Parse each line to collect data and find max coordinates
    data = []
    max_x = 0
    max_y = 0
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(',', 2)  # Split into three parts
        if len(parts) != 3:
            continue  # Skip lines that don't split into exactly three parts
        try:
            x = int(parts[0].strip())
            y = int(parts[1].strip())
        except ValueError:
            continue  # Skip lines with invalid integers for x or y
        char = parts[2]  # Keep the character as-is, including any spaces
        data.append((x, y, char))
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    
    # Create the grid filled with spaces
    rows = max_y + 1
    cols = max_x + 1
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    
    # Fill in the characters from the data
    for x, y, char in data:
        if 0 <= y < rows and 0 <= x < cols:
            grid[y][x] = char
    
    # Print each row of the grid
    for row in grid:
        print(''.join(row))