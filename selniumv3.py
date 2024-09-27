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

    # Loop through each row and check for the target string
    for row_index, row in enumerate(rows):
        print(f"Checking row {row_index + 1}...")

        # Find all cells in the current row
        cells = row.find_elements(By.CLASS_NAME, "rich-table-cell")

        # Check if the target string exists in any cell of the current row
        found_target = False
        for cell_index, cell in enumerate(cells):
            cell_text = cell.text
            print(f"Row {row_index + 1}, Cell {cell_index + 1}: {cell_text}")

            # Check if the cell contains the target string
            if "target_string" in cell_text:  # Replace with your actual target string
                print(f"String 'target_string' found in Row {row_index + 1}, Cell {cell_index + 1}")
                found_target = True
                break  # Stop checking other cells once the target string is found

        # If the target string was found, click the link in the first cell of the same row
        if found_target and cells:
            # Assuming the link is in the first cell (index 0)
            link_cell = cells[0]
            link = link_cell.find_element(By.TAG_NAME, "a")  # Assuming the link is an <a> tag
            
            # Click the link
            link.click()
            print("Clicked the link in the first cell.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()
