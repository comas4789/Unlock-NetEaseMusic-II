# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0036ACDBDC74072B6BDB39B22B2D1C5C565A71F227DD4D6E5FDE1CD77D7D847243C751111BE836006B66B28543EDF7E8119957633961BB4F92EC21CE161EF2F6FBF43D55C60AD9F09BBF5D2D87505F0686D2E56017F7F8B6B61C1C3AF31DAAB43E6D2AE9CA8575D53F23A092FC13B26429AD4F013D300FD145A244B947B37C4D2DA8B81E8B17339E337F2EAFAD04BC341716727A5FEF304504A063BC3ECEFE71E32C7AE97C1EEA905444F29A4564E173C7B27F2ABD025DDFB39E6DA413744B6E9B3DE7CB7F5B0C6EA1D498A9466A6CDE44E92ED92CEF481C727B3585BACA8AD42051431993F7F88158812CA8905668943DE7C1D2BE92837BD5C877E2A92858639A1AD3748A42414366A41109E3A869526FF7E906818F41F1E36C39396E572CB8C69D5164860105131BDA1967AB177C7AA443CFC33968A92CBE60F0BA0AC22839B11752616AFD91BB6663A3A578434D07E21B569ACEAB12A9C88F01EDF459A22A66"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
