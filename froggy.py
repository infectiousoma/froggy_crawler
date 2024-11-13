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
    options = webdriver.FirefoxOptions()
    options.binary_location = '/snap/firefox/current/usr/lib/firefox/firefox'
    driver = webdriver.Firefox(options=options)
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
    # Load the login page and wait for manual login
    driver.get(LOGIN_URL)
    print("Please complete the login process manually.")
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, "//div/input[@type='text']"))
    )
    input("Press Enter after completing the login...")

    # Once logged in, go to the frog page
    driver.get(BASE_URL)
    entries = driver.find_elements(By.XPATH, '/html/body/div/table/tbody/tr')
    urls = {}
    for entry in entries:
        try:
            index_text = entry.find_element(By.XPATH, './td[1]').text
            # Ensure the index text is numeric before converting to int
            if index_text.isdigit():
                index = int(index_text)
                url = entry.find_element(By.XPATH, './td[2]/a').get_attribute('href')
                urls[index] = url
            else:
                print(f"Skipping non-numeric index: {index_text}")
        except Exception as e:
            print(f"Failed to process entry: {str(e)}")
    return urls

def crawl(driver, urls, start_index):
    sorted_urls = {k: urls[k] for k in sorted(urls) if k >= start_index}

    try:
        for index in sorted_urls:
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

            save_index(index + 1)  # Save the next index to start from

    finally:
        # Don't close the driver here, keep it open until all processing is done
        pass

if __name__ == "__main__":
    start_index = get_start_index()
    
    driver = load_driver()
    urls = get_frog_urls(driver)
    
    crawl(driver, urls, start_index)
    
    driver.quit()  # Quit the driver after all work is done
