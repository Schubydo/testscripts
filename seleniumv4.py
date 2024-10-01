import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_excel_files(download_dir):
    """
    Returns a set of existing Excel files in the download directory.
    """
    return {file.lower() for file in os.listdir(download_dir) if file.lower().endswith(('.xls', '.xlsx'))}

def clean_downloads_folder(download_dir):
    """
    Cleans the downloads folder by deleting files that are not Excel files (.xls, .xlsx).
    """
    import glob
    files = glob.glob(os.path.join(download_dir, "*"))

    for file in files:
        if not file.lower().endswith(('.xls', '.xlsx')):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Failed to delete {file}: {str(e)}")

# Set the desired download location
download_dir = '/path/to/your/custom/download/directory'

# Set Edge options
edge_options = Options()
edge_options.add_experimental_option('prefs', {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Initialize the WebDriver with the custom options
driver = webdriver.Edge(options=edge_options)

# Open the webpage containing the grid
driver.get('your_website_url')

# Wait until gridxBody is available
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'gridxBody'))
)

# Locate the gridxBody container
gridx_body = driver.find_element(By.CLASS_NAME, 'gridxBody')

# Wait for rows to be present (gridxRow elements)
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.gridxBody .gridxRow'))
)

# Locate all gridxRow elements (grab only the first 5)
rows = gridx_body.find_elements(By.CSS_SELECTOR, '.gridxRow')

# Initialize ActionChains for double-clicking
actions = ActionChains(driver)

# Loop over the first 5 rows or until a new Excel file is downloaded
for i in range(min(5, len(rows))):
    row = rows[i]  # Get the i-th row
    
    # Wait for the specific cell to be present in the DOM
    cell = WebDriverWait(row, 10).until(
        EC.presence_of_element_located((By.XPATH, './/td[@colid="7"]'))
    )
    
    # Scroll to the cell element
    driver.execute_script("arguments[0].scrollIntoView(true);", cell)

    # Wait for the cell to be clickable
    cell = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, './/td[@colid="7"]'))
    )
    
    # Print the text of the cell
    cell_text = cell.text
    print(f"Text in cell of row {i+1}: {cell_text}")

    # Attempt to double-click using ActionChains
    try:
        actions.double_click(cell).perform()
    except Exception as e:
        print(f"Failed to double-click using ActionChains: {str(e)}")
        # Fallback to JavaScript double-click
        driver.execute_script("var evt = new MouseEvent('dblclick', { bubbles: true, cancelable: true }); arguments[0].dispatchEvent(evt);", cell)

    # Wait for a moment to allow the download to initiate
    time.sleep(2)  # Adjust as necessary

# Optionally: Clean the downloads folder
clean_downloads_folder(download_dir)

# Close the driver
driver.quit()
