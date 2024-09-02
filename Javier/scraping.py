# Import the requests library to make HTTP requests
import requests
# Import the BeautifulSoup class from the bs4 module for parsing HTML
from bs4 import BeautifulSoup
import urllib3
import time

# Import the necessary classes and modules from the Selenium library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Define the URL of the web page to scrape
url = 'https://inside.fifa.com/fifa-world-ranking/men'

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

driver.get(url)
WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    ).click()
#time.sleep(10)
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"table")))
table_html = driver.execute_script("""
    var table = document.querySelector('table');
    return table ? table.outerHTML : '';
""")

#tables = driver.find_element(By.CSS_SELECTOR, "table")
#print(tables.get_attribute('innerTEXT'))
#print('1:',tables)
#table_html = driver.execute_script("return document.querySelector('table').outerHTML")
soup = BeautifulSoup(table_html, 'html.parser')

rows = soup.find_all('tr')
#print('\nrows: ')
#print(rows)

data = []
print('\ncols:')
for row in rows:
    cols = row.find_all('a')
    cols = [col.text.strip() for col in cols]  #
    print(cols)
    data.append(cols)
print(data)

time.sleep(10)
table_html_2 = driver.execute_script("""
    var table = document.querySelector('table');
    return table ? table.outerHTML : '';
""")
soup_2 = BeautifulSoup(table_html_2, 'html.parser')

rows_2 = soup.find_all('tr')
#print('\nrows: ')
#print(rows)

data_2 = []
print('\ncols:')
for row in rows_2:
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]  #
    print(cols)
    data_2.append(cols)
print(data_2)

# rows = tables.find_elements(By.TAG_NAME, "tr")
# print(rows)
# for row in rows:
#     columns = row.find_elements(By.TAG_NAME, "td")
#     # print(row)
#     # print(columns)
print('----------------'*10)


# Send a GET request to the specified URL, disabling SSL verification
response = requests.get(url, verify=False)

# Create a BeautifulSoup object to parse the HTML content of the response
soup = BeautifulSoup(response.text, 'html.parser')
# print('-------SOUP-----'*10)
# print(soup)
# print('-------SOUP-----'*10)


# Find all <ol> (ordered list) elements on the page
ordered_lists = soup.find_all('table')
print('2:',ordered_lists)
#<table class="table-module_table__76hUL fcds-table" role="table">

# Initialize a list to store all quotes
all_quotes = []

# Iterate over each ordered list (there are multiple)
for ordered_list in ordered_lists:
    # Find all <li> (list item) elements within the current <ol> element
    quotes = ordered_list.find_all('li')
    
    # Iterate over the list of quotes and add them to the all_quotes list
    for quote in quotes:
        # Get the text content of each quote, stripping leading/trailing whitespace
        quote_text = quote.get_text(strip=True)
        all_quotes.append(quote_text)

# Iterate over the all_quotes list with an index starting from 1 and print each quote
for idx, quote in enumerate(all_quotes, 1):
    # Print the index and the quote text in a formatted string
    print(f"{idx}. {quote}")


# def scrape_fifa_rankings(gender):
#     """
#     Scrape FIFA rankings for the specified gender (male or female).
#     :param gender: 'male' for men's rankings, 'female' for women's rankings.
#     :return: List of lists containing rank, country, and points.
#     """
#     if gender == 'male':
#         url = "https://inside.fifa.com/fifa-world-ranking/men"
#     elif gender == 'female':
#         url = "https://inside.fifa.com/fifa-world-ranking/women"
#     else:
#         raise ValueError("Invalid gender. Use 'male' or 'female'.")

#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     rankings = []
    
#     # Find the table containing rankings
#     table = soup.find('table', {'class': 'table-module_table__76hUL fcds-table'})
#     if table:
#         rows = table.find_all('tr')[1:]  # Skip the header row
#         for row in rows:
#             cols = row.find_all('td')
#             rank = cols[0].text.strip()
#             country = cols[1].text.strip()
#             points = cols[2].text.strip()
#             rankings.append([rank, country, points])
#     else:
#         print("Ranking table not found on the page.")

#     return rankings

# # Scrape men's rankings
# men_rankings = scrape_fifa_rankings('male')
# print("Men's FIFA Rankings:")
# for rank in men_rankings[:10]:  # Displaying top 10 for brevity
#     print(rank)

# # Scrape women's rankings
# women_rankings = scrape_fifa_rankings('female')
# print("\nWomen's FIFA Rankings:")
# for rank in women_rankings[:10]:  # Displaying top 10 for brevity
#     print(rank)

