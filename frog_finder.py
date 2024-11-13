from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import threading

# Constants
LOGIN_URL = "https://zupass.org/#/login"  # Adjust this to the actual login URL
# Define your iframe XPath (make sure it's correct)
IFRAME_XPATH = "/html/body/div/div/div/div/div[2]/iframe"  # Adjust this to the correct iframe XPath
SECOND_BUTTON_XPATH = "/html/body/div/div[2]/div[2]/main/div/div[2]/div[1]/button"  # Adjust this XPath

def load_driver():
    """Load the Firefox WebDriver with necessary options."""
    options = webdriver.FirefoxOptions()
    options.binary_location = '/snap/firefox/current/usr/lib/firefox/firefox'
    driver = webdriver.Firefox(options=options)
    return driver

def click_second_button(driver):
    """Click the second button every 15 minutes inside an iframe."""
    while True:
        try:
            # Wait for the iframe to be available and switch to it
            print("Waiting for the iframe to be available...")
            iframe = WebDriverWait(driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, IFRAME_XPATH))
            )
            print("Switched to the iframe.")

            # Wait for the second button to be clickable within the iframe
            print("Waiting for the second button to be clickable...")
            second_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, SECOND_BUTTON_XPATH))
            )
            print("Second button is now clickable!")

            # Perform the click
            second_button.click()
            print("Clicked the second button!")

            # Switch back to the default content after clicking the button
            driver.switch_to.default_content()
            print("Switched back to the main content.")

            # Wait for 15 minutes before clicking again
            time.sleep(15 * 60)  # 15 minutes in seconds

        except Exception as e:
            print("Error clicking the second button:", str(e))

def crawl(driver):
    """Main crawling function to manage login and interactions."""
    # Load the login page and wait for manual login
    driver.get(LOGIN_URL)
    print("Please complete the login process manually.")
    
    # Wait for the presence of an element that indicates the user is logged in
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, "//div/input[@type='text']"))
    )
    
    # Allow the user to manually complete the login process
    input("Press Enter after completing the login...")

    # Start a background thread to click the second button every 15 minutes
    threading.Thread(target=click_second_button, args=(driver,), daemon=True).start()

if __name__ == "__main__":
    driver = load_driver()
    
    try:
        # Start the crawling process
        crawl(driver)

        # Keep the script running to maintain the periodic task (15 minutes)
        while True:
            time.sleep(1)  # Keep the main thread alive
    finally:
        driver.quit()  # Quit the driver when done
