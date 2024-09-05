from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# List of topics to search
topic = "Manchester United FC"

# Open Google
driver.get("https://www.google.com?hl=en")

# Accept cookies if the button appears
try:
    accept_cookies = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='Reject all']"))    )
    accept_cookies.click()    
except:
    pass  # If the accept cookies button doesn't appear, continue
time.sleep(2)
# Find the search box, enter the topic, and press Enter
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(topic)
time.sleep(1)
search_box.send_keys(Keys.RETURN)

# Wait for the results page to load and display the results
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "search"))
)
try:
    # Locate all elements in the "About" section using a generalized XPath
    about_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'zloOqf')]/div"))
    )
    
    # Extract and print each piece of information
    print(f"Information about {topic}:")
    for item in about_items:
        print(item.text)  # Correctly accessing the text attribute of each element
    print('-' * 60)
except Exception as e:
    print(f"Could not find information for {topic}. Error: {e}")

# Wait a few seconds before the next search (to avoid issues with Google)
time.sleep(3)

# Close the browser
driver.quit()


