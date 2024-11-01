import re
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up WebDriver
driver = webdriver.Chrome()  # Replace with the path to your WebDriver
driver.get("URL_OF_YOUR_PAGE")  # Replace with the actual URL of your page

try:
    # Find all elements with an ID that starts with "dijit_TreeNode_"
    elements = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'dijit_TreeNode_')]")

    # Extract numbers from the IDs and find the largest one
    max_number = -1  # Start with a minimum value
    for elem in elements:
        match = re.search(r"dijit_TreeNode_(\d+)", elem.get_attribute("id"))
        if match:
            node_number = int(match.group(1))
            max_number = max(max_number, node_number)

    print("Largest number in dijit_TreeNode_* IDs:", max_number)

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
ß