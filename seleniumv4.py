import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
    first_cell = row.find_element(By.CSS_SELECTOR, '.gridxRowTable .gridxCell')

    # Scroll to the element to ensure it's visible
    driver.execute_script("arguments[0].scrollIntoView(true);", first_cell)

    # Make sure the element is visible and interactable
    WebDriverWait(driver, 10).until(EC.visibility_of(first_cell))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(first_cell))

    # Try double-clicking using ActionChains
    try:
        actions.double_click(first_cell).perform()
    except Exception as e:
        print(f"Failed to double-click using ActionChains: {str(e)}")
        # Fallback to JavaScript double-click
        driver.execute_script(
            "var evt = new MouseEvent('dblclick', { bubbles: true, cancelable: true }); arguments[0].dispatchEvent(evt);",
            first_cell
        )

    # Wait for a moment to allow the download to initiate
    time.sleep(2)  # Adjust as necessary

# Close the driver
driver.quit()

