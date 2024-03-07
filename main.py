from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import os
from dotenv import load_dotenv
import smtplib

# -------------- CONSTANTS ---------------- #



# ------------ WEBSITE TO MONITOR ---------------- #
# Undeveloped UI to make it easier to input a target amazon product to monitor.
website_to_monitor = input("Please input the website link you would like to monitor: ")


# ------------ CONFIGURE HEADLESS BROWSER ------------ #
# This is used to bypass the captcha without the user having to interface with anything. It simply runs in the console.

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)
driver.get(website_to_monitor)


# ------------- INFO EXTRACTION ----------------- #
# Once past the captcha, this code sifts through the HTML to locate price. Since the price is separated in the HTML between dollars and cents, we have to peice the two values together.

# Get the page source using Selenium ->
html_content = driver.page_source

# Use BeautifulSoup to parse the HTML content ->
soup = BeautifulSoup(html_content, 'html.parser')

# Locate and extract the price info
dollar_price_element = soup.find(class_="a-price-whole")
fraction_price_element = soup.find(class_="a-price-fraction")

# Check if both elements are found ->
if dollar_price_element and fraction_price_element:
    # Clean up the extracted prices
    dollar_price = re.sub(r'[^\d]', '', dollar_price_element.text)
    fraction_price = re.sub(r'[^\d]', '', fraction_price_element.text)

    # Convert the cleaned prices to float ->
    price = float(f"{dollar_price}.{fraction_price}")
    print(price)
else:
    print("Price elements not found or the format is unexpected.")

# Close the browser ->
driver.quit()


# ---------------- PRICE COMPARISON -------------- #
# This code takes the price scraped from the website and compares it against a predetermined value. If it reaches a certain threshold, an email will be generated and sent to the recipient.




# ---------------- EMAIL GENERATION -------------- #
# the sender and receiver email info is stored separately for security reasons. This code uses the smtplib library to establish a secure connection between sender and receiver. To send the email, simply pass through a message to the send_email function.

# Load environment variables from .env file ->
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'api_info.env'))

sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")

def email_provider():
    # Function sifts through provided email and returns SMTP Host info.

    SMTP_HOST_INFO = {
        "gmail": "smtp.gmail.com",
        "hotmail": "smtp.live.com",
        "yahoo": "smtp.mail.yahoo.com"
    }
    if "gmail" in sender_email:
        return SMTP_HOST_INFO["gmail"]
    elif "yahoo" in sender_email:
        return SMTP_HOST_INFO["yahoo"]
    elif "hotmail" in sender_email:
        return SMTP_HOST_INFO["hotmail"]
    else:
        print("Unknown E-mail Provider.")

def send_email(message):
    # Send info over via new e-mail to desired e-mail.

    connection = smtplib.SMTP(email_provider()) 
    connection.starttls()  # Encrypts e-mail
    connection.login(user=sender_email, password=sender_password)
    connection.sendmail(
        from_addr=sender_email,
        to_addrs=receiver_email,
        msg=message
    )
    connection.close()