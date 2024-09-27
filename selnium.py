from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver (for example, using Chrome)
driver = webdriver.Chrome()

# Navigate to the webpage containing the tree
driver.get('http://your-webpage-url.com')

try:
    # Locate the specific tree node label (e.g., 'dijit_TreeNode_3_label')
    node_label = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dijit_TreeNode_3_label"))
    )
    
    # Find the expandoNode related to the tree node (preceding or sibling element)
    # Adjust this XPath according to your DOM structure
    expando_node = node_label.find_element(By.XPATH, "./preceding-sibling::div[contains(@class, 'dijitTreeExpando')]")
    
    # Ensure the expandoNode's parent or relevant element is collapsed (aria-expanded="false")
    parent_node = expando_node.find_element(By.XPATH, "../..")  # Move up to parent div with aria-expanded
    if parent_node.get_attribute("aria-expanded") == "false":
        print("Node is collapsed. Expanding it.")

        # Click the expandoNode to expand the tree node
        expando_node.click()

        # Optionally, wait until aria-expanded becomes "true"
        WebDriverWait(driver, 10).until(
            EC.attribute_to_be((By.XPATH, "//*[@id='dijit_TreeNode_3_label']/../.."), "aria-expanded", "true")
        )
        print("Node is now expanded.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()
