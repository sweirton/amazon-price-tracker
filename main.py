from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import logging


# ------------ WEBSITE TO MONITOR ---------------- #
website_to_monitor = input("Please input the website link you would like to monitor: ")

# ------------ CONFIGURE HEADLESS BROWSER -------------- #
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

driver = webdriver.Chrome(options=chrome_options)
driver.get(website_to_monitor)

# ------------- PAGE EXTRACTION ----------------- #
# Get the page source using Selenium
html_content = driver.page_source

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Locate and extract the price info
dollar_price_element = soup.find(class_="a-price-whole")
fraction_price_element = soup.find(class_="a-price-fraction")

# Check if both elements are found
if dollar_price_element and fraction_price_element:
    # Clean up the extracted prices
    dollar_price = re.sub(r'[^\d]', '', dollar_price_element.text)
    fraction_price = re.sub(r'[^\d]', '', fraction_price_element.text)

    # Convert the cleaned prices to float
    final_price = float(f"{dollar_price}.{fraction_price}")
    print(final_price)
else:
    print("Price elements not found or the format is unexpected.")

# Close the browser
driver.quit()
