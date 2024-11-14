import os
from dotenv import load_dotenv

from telethon import TelegramClient, events, sync
from telethon.tl.types import PeerChannel

load_dotenv()

api_id = os.getenv('TELEGRAM_APP_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

client = TelegramClient('session_name', api_id, api_hash)
client.start()

def is_frog_link(link):
    if link is None:
        return False, None 
    link = link.split(' ')[0]

    if "-" not in link:
        return False, None
    
    found = link.startswith('http://dc7.getfrogs.xyz/necklace/') or link.startswith('https://dc7.getfrogs.xyz/necklace/')

    if link.startswith('http://'):
        link = link.replace('http://', 'https://')

    return found, link[0:70]

frog_channel = client.get_entity(PeerChannel(2090633646))

messages = client.get_messages(frog_channel, limit=1000)

frog_links = []

for message in messages:
    found, link = is_frog_link(message.text)
    if found:
        frog_links.append(link)
        print(link)


frog_links = list(set(frog_links))

print(f"Found {len(frog_links)} frog links")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Constants
BASE_URL = "https://frog.geek.sg/"
LOGIN_URL = "https://zupass.org/#/login"  # Adjust this to the actual login URL
START_INDEX_FILE = "last_index.txt"
BATCH_SIZE = 5  # Set this to 1, 5, 10, or any other number based on your needs

def load_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    return driver

def get_start_index():
    try:
        with open(START_INDEX_FILE, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 336  # Default start index if file not found

def save_index(index):
    with open(START_INDEX_FILE, "w") as file:
        file.write(str(index))

def get_frog_urls(driver):
    return frog_links

def crawl(driver, urls, start_index):
    sorted_urls = urls 
    driver.get(LOGIN_URL)
    print("Please complete the login process manually.")
    
    # Wait for the presence of an element that indicates the user is logged in
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, "//div/input[@type='text']"))
    )
    
    # Allow the user to manually complete the login process
    input("Press Enter after completing the login...")

    try:
        for index in range(start_index, len(sorted_urls)): 
            driver.get(sorted_urls[index])
            time.sleep(5)  # Wait for the page to load
            
            try:
                # Switch to the iframe (assuming it's the first iframe on the page)
                iframe = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "iframe"))
                )
                driver.switch_to.frame(iframe)  # Switch to the iframe
                
                # Wait for the button to be clickable inside the iframe and click it
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div/div/button[1]"))
                ).click()

                # Optionally, wait for an element in the new page to load (if the page redirects)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='unique_element_on_next_page']"))
                )

                print(f"Entry {index}: Clicked the button, ignoring response.")
                time.sleep(3)  # Wait for 3 seconds before opening the next URL
                
                # Switch back to the main content after interacting with the iframe
                driver.switch_to.default_content()
                
            except Exception as e:
                print(f"Error processing entry {index}: {str(e)}")

            save_index(index + 1)

    finally:
        # Don't close the driver here, keep it open until all processing is done
        pass

if __name__ == "__main__":
    start_index = get_start_index()
    
    driver = load_driver()
    urls = get_frog_urls(driver)
    
    crawl(driver, urls, start_index)
    
    driver.quit()  # Quit the driver after all work is done




