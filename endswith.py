from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver and load the page
driver = webdriver.Chrome()
driver.get("your_url_here")

# Wait until the parent tree node is loaded
wait = WebDriverWait(driver, 10)
parent_tree_node = wait.until(EC.presence_of_element_located((By.XPATH, "your_parent_node_xpath_here")))

# Now find all descendant nodes with the 'dijit_tree_node' class within this parent node
child_nodes = parent_tree_node.find_elements(By.XPATH, ".//div[contains(@class, 'dijit_tree_node')]")

# Print the number of child nodes
print("Number of child nodes:", len(child_nodes))

# Close the driver
driver.quit()
