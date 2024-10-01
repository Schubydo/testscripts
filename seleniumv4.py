import os
import time
import logging
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

class WebDriverAutomation:
    def __init__(self, download_dir, log_file_name):
        self.download_dir = download_dir
        self.log_file_name = log_file_name
        self.driver = None
        self.logger = self.create_logger()

        # Ensure the download directory exists
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        # Set Edge options
        edge_options = Options()
        edge_options.add_experimental_option('prefs', {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        edge_options.add_argument('--start-maximized')  # Start maximized to ensure all elements are visible

        # Initialize the WebDriver
        self.driver = webdriver.Edge(options=edge_options)

    def create_logger(self):
        """Sets up the logger for the class."""
        logger = logging.getLogger('WebDriverAutomation')
        logger.setLevel(logging.DEBUG)
        
        # Create a file handler
        fh = logging.FileHandler(self.log_file_name)
        fh.setLevel(logging.DEBUG)

        # Create a console handler (optional)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Create a formatter and set it for both handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger

    def run(self, website_url, iframe_selector):
        """Main function to run the WebDriver tasks."""
        try:
            self.logger.info("Opening the webpage.")
            # Open the webpage
            self.driver.get(website_url)

            # Wait for the page to fully load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )

            # If the grid is inside an iframe, switch to it
            try:
                iframe = self.driver.find_element(By.CSS_SELECTOR, iframe_selector)
                self.driver.switch_to.frame(iframe)
                self.logger.info("Switched to iframe.")
            except NoSuchElementException:
                self.logger.warning("No iframe found. Continuing without switching.")

            # Wait until gridxBody is available
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'gridxBody'))
            )

            # Locate the gridxBody container
            gridx_body = self.driver.find_element(By.CLASS_NAME, 'gridxBody')

            # Wait for rows to be present
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.gridxBody .gridxRow'))
            )

            # Locate all gridxRow elements (grab only the first 5)
            rows = gridx_body.find_elements(By.CSS_SELECTOR, '.gridxRow')
            self.logger.info(f"Found {len(rows)} rows.")

            if not rows:
                raise Exception("No rows found in the grid.")

            # Initialize ActionChains for double-clicking
            actions = ActionChains(self.driver)

            # Loop over the first 5 rows
            for i in range(min(5, len(rows))):
                try:
                    row = rows[i]  # Get the i-th row
                    self.logger.info(f"Processing row {i+1}")

                    # Locate the first cell within the row
                    first_cell = row.find_element(By.CSS_SELECTOR, '.gridxRowTable .gridxCell')
                    self.logger.info(f"Located first cell of row {i+1}")

                    # Scroll to the element to ensure it's visible
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", first_cell)
                    self.logger.info(f"Scrolled to row {i+1}")

                    # Wait for any potential animations to complete
                    time.sleep(1)

                    # Ensure the element is visible and clickable
                    WebDriverWait(self.driver, 20).until(EC.visibility_of(first_cell))
                    WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(first_cell))
                    self.logger.info(f"Row {i+1} is visible and clickable.")

                    # Try double-clicking using ActionChains
                    try:
                        actions.double_click(first_cell).perform()
                        self.logger.info(f"Double-clicked row {i+1} using ActionChains.")
                    except (ElementNotInteractableException, StaleElementReferenceException) as e:
                        self.logger.warning(f"ActionChains failed for row {i+1}: {str(e)}")
                        # Fallback to JavaScript double-click
                        self.driver.execute_script(
                            "var evt = new MouseEvent('dblclick', { bubbles: true, cancelable: true }); arguments[0].dispatchEvent(evt);",
                            first_cell
                        )
                        self.logger.info(f"Double-clicked row {i+1} using JavaScript.")

                    # Wait for the download to initiate
                    time.sleep(3)  # Adjust as necessary based on download initiation time

                except TimeoutException as te:
                    self.logger.error(f"Timeout while processing row {i+1}: {str(te)}")
                    # Take a screenshot for debugging
                    self.driver.save_screenshot(f'screenshot_row_{i+1}_timeout.png')
                except Exception as e:
                    self.logger.error(f"An error occurred while processing row {i+1}: {str(e)}")
                    # Take a screenshot for debugging
                    self.driver.save_screenshot(f'screenshot_row_{i+1}_error.png')

        finally:
            # Close the driver after all operations
            self.driver.quit()
            self.logger.info("Driver closed.")

# Usage Example:
if __name__ == "__main__":
    download_dir = '/path/to/your/custom/download/directory'
    log_file_name = '/path/to/your/log/file.log'
    website_url = 'your_website_url'
    iframe_selector = 'iframe#iframe_id_or_selector'

    automation = WebDriverAutomation(download_dir, log_file_name)
    automation.run(website_url, iframe_selector)

