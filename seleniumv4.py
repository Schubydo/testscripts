import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)

# Set the desired download location
download_dir = '/path/to/your/custom/download/directory'

# Ensure the download directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Set Edge options
edge_options = Options()
edge_options.add_experimental_option('prefs', {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
edge_options.add_argument('--start-maximized')  # Start maximized to ensure all elements are visible

# Initialize the WebDriver with the custom options
driver = webdriver.Edge(options=edge_options)

try:
    # Open the webpage containing the grid
    driver.get('your_website_url')

    # Optional: Wait for the page to fully load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # If the grid is inside an iframe, switch to it
    try:
        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe#iframe_id_or_selector')
        driver.switch_to.frame(iframe)
        print("Switched to iframe.")
    except NoSuchElementException:
        print("No iframe found. Continuing without switching.")

    # Wait until gridxBody is available
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'gridxBody'))
    )

    # Locate the gridxBody container
    gridx_body = driver.find_element(By.CLASS_NAME, 'gridxBody')

    # Wait for rows to be present (gridxRow elements)
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.gridxBody .gridxRow'))
    )

    # Locate all gridxRow elements (grab only the first 5)
    rows = gridx_body.find_elements(By.CSS_SELECTOR, '.gridxRow')
    print(f"Found {len(rows)} rows.")

    if not rows:
        raise Exception("No rows found in the grid.")

    # Initialize ActionChains for double-clicking
    actions = ActionChains(driver)

    # Loop over the first 5 rows or until a new Excel file is downloaded
    for i in range(min(5, len(rows))):
        try:
            row = rows[i]  # Get the i-th row
            print(f"Processing row {i+1}")

            # Locate the first cell within the row
            first_cell = row.find_element(By.CSS_SELECTOR, '.gridxRowTable .gridxCell')
            print(f"Located first cell of row {i+1}")

            # Scroll to the element to ensure it's visible
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", first_cell)
            print(f"Scrolled to row {i+1}")

            # Optional: Wait for any potential animations to complete
            time.sleep(1)

            # Ensure the element is visible and clickable
            WebDriverWait(driver, 20).until(EC.visibility_of(first_cell))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(first_cell))
            print(f"Row {i+1} is visible and clickable.")

            # Try double-clicking using ActionChains
            try:
                actions.double_click(first_cell).perform()
                print(f"Double-clicked row {i+1} using ActionChains.")
            except (ElementNotInteractableException, StaleElementReferenceException) as e:
                print(f"ActionChains failed for row {i+1}: {str(e)}")
                # Fallback to JavaScript double-click
                driver.execute_script(
                    "var evt = new MouseEvent('dblclick', { bubbles: true, cancelable: true }); arguments[0].dispatchEvent(evt);",
                    first_cell
                )
                print(f"Double-clicked row {i+1} using JavaScript.")

            # Wait for the download to initiate
            time.sleep(3)  # Adjust as necessary based on download initiation time

            # Optionally, verify the download has started by checking the download directory
            # (Implementation depends on the specific download behavior)

        except TimeoutException as te:
            print(f"Timeout while processing row {i+1}: {str(te)}")
            # Optional: Take a screenshot for debugging
            driver.save_screenshot(f'screenshot_row_{i+1}_timeout.png')
        except Exception as e:
            print(f"An error occurred while processing row {i+1}: {str(e)}")
            # Optional: Take a screenshot for debugging
            driver.save_screenshot(f'screenshot_row_{i+1}_error.png')

finally:
    # Close the driver after all operations
    driver.quit()
    print("Driver closed.")


