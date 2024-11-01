from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver and load the page
driver = webdriver.Chrome()
driver.get("your_url_here")

# Set the unique identifier for the parent node
parent_id = "dijit__TreeNode_3"

# Wait until the parent tree node is loaded
wait = WebDriverWait(driver, 10)
parent_tree_node = wait.until(EC.presence_of_element_located((By.ID, parent_id)))

# Find all child nodes with an ID pattern starting with 'dijit__TreeNode_' under the parent
# Assuming they are direct children or descendants
child_nodes = parent_tree_node.find_elements(By.XPATH, ".//div[starts-with(@id, 'dijit__TreeNode_') and not(@id='" + parent_id + "')]")

# Print the number of child nodes
print("Number of child nodes:", len(child_nodes))

# Close the driver
driver.quit()
