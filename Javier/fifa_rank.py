from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import Tables_are_fun
from Tables_are_fun import insert_land

def fifa_rank():
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


    url = 'https://uk.soccerway.com/teams/rankings/fifa/' #male
    driver = webdriver.Chrome(options=chrome_options)  # or use 'webdriver.Firefox()' for Firefox
    driver.get(url)
    WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()

    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #print(soup)

    # Close the browser
    driver.quit()
    # Now try finding the table
    table = soup.find('table', {'class': 'leaguetable table fifa_rankings'})
    #print(table)

    rows = table.find('tbody').find_all('tr')
    #rows = table.find_all('tr', {'class': 'odd'})

    for row in rows:
        #print(row)
        try:
            rank = row.find('td', {'class': 'rank'}).text.strip()
            nationality = row.find('td', {'class': 'text team'}).find('a').text.strip()
            points = row.find('td', {'class': 'points'}).text.strip()
            print(nationality, rank, points)
            insert_land([nationality, rank, points])
        except:
            pass
    

#fifa_rank()