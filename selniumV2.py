from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up WebDriver (e.g., using Chrome)
driver = webdriver.Chrome()

# Navigate to the webpage containing the rich-table
driver.get('http://your-webpage-url.com')

try:
    # Locate the rich-table
    rich_table = driver.find_element(By.CLASS_NAME, "rich-table")

    # Find all rows in the rich-table
    rows = rich_table.find_elements(By.CLASS_NAME, "rich-table-row")
    
    # Get the total number of rows
    row_count = len(rows)
    print(f"Total number of rows: {row_count}")
    
    # Loop through each row and check for the string in each cell
    for row_index, row in enumerate(rows):
        print(f"Checking row {row_index + 1}...")
        
        # Find all cells in the current row
        cells = row.find_elements(By.CLASS_NAME, "rich-table-cell")
        
        # Loop through each cell and check if it contains the target string
        for cell_index, cell in enumerate(cells):
            cell_text = cell.text
            print(f"Row {row_index + 1}, Cell {cell_index + 1}: {cell_text}")
            
            # Check if the cell contains the target string
            if "target_string" in cell_text:
                print(f"String 'target_string' found in Row {row_index + 1}, Cell {cell_index + 1}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()
