from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up WebDriver
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get('http://your-webpage-url.com')

try:
    # Locate the specific tree node label
    node_label = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dijit_TreeNode_3_label"))
    )

    # Locate the expandoNode using XPath (based on sibling or nearby structure)
    # This assumes the expandoNode is adjacent to the label, adjust XPath as necessary
    expando_node = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@id='dijit_TreeNode_3_label']/preceding-sibling::div[contains(@class, 'dijitTreeExpando')]"))
    )

    # Ensure the parent or related element is collapsed (aria-expanded="false")
    parent_node = expando_node.find_element(By.XPATH, "../..")  # Go up to the parent node containing aria-expanded
    if parent_node.get_attribute("aria-expanded") == "false":
        print("Node is collapsed. Expanding it.")
        
        # Click the expandoNode to expand the tree node
        expando_node.click()

        # Optionally, wait until aria-expanded becomes "true"
        WebDriverWait(driver, 10).until(
            EC.attribute_to_be((By.XPATH, "//div[@id='dijit_TreeNode_3']"), "aria-expanded", "true")
        )
        print("Node is now expanded.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()
