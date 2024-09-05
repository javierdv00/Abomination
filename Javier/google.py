from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# List of topics to search
topic = "Manchester United FC"


# Set up Chrome options to run in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model, necessary for certain environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--window-size=1920,1080")  # Set a large window size
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Set a user-agent
count_page = 0

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)  # or use 'webdriver.Firefox()' for Firefox

# Open Google
driver.get("https://www.google.com?hl=en")

# Accept cookies if the button appears
try:
    accept_cookies = WebDriverWait(driver, 5).until(
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
manager, stadium, location, founded, leagues = '','','','',''

try:
    # Locate all elements in the "About" section using a generalized XPath
    about_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'zloOqf')]/div"))
    )
    for item in about_items:
        if ":" in item.text:
            label, value = item.text.split(":",1)
            #print(label,":", value)
            if label.lower() in ['manager', 'coach', 'trainer']:
                manager = value.strip()
            if label.lower() in ['location', 'locations']:
                location = value.strip()
            if label.lower() in ['founded']:
                founded = value.strip()
            if label.lower() in ['arena', 'stadium', 'ground', 'arena/stadium', 'stadium/arena']:
                stadium = value.strip()
            if label.lower() in ['leagues', 'league']:
                leagues = value.strip()
            
    print(manager,'/', stadium,'/', location,'/', founded,'/', leagues)
except Exception as e:
    print(f"Could not find information for {topic}. Error: {e}")

# Wait a few seconds before the next search (to avoid issues with Google)
#time.sleep(3)

# Close the browser
driver.quit()


