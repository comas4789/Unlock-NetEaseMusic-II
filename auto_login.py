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
    browser.add_cookie({"name": "MUSIC_U", "value": "00617D209714219F0D16079C390C176A31A7230CFFB6CDBEECACE232F6C75DD9B3944F298FEAFC9F5893B66AE22C716850F6A55C871CE5D59AB1DA2AB92166240E43F2170FF53115EA99AB42573FD8A5D478B12E25C62043C2A79BC8AE7D2CD4416DAC7A051F652C7699C0DEDEA4F3F7BBE645DAFC37434B14E8221B90B193426A36E76DCD0CB81EA5BF3C4CEC5C358EC75CB1987575E3B77D77561EA2E93799F4D89E15BFC166688FC4BDC94BFEAC314C20D74E12CD9E51BB5570AD136A24E9C9E33F6A11A8B71627312AC1FE5A738D424B4CF3CFB9D12012A74AB6C6D837F45BEC400BE8A3E3E910DFCD8D9004DA9A12F7F508CA4278F75F808E13CA119206F264043121C27B8673EFAEDECAA305E168513CBF7E6A50D8EDB1AD50A9DEE6B5B5A166BA68DB749AE2CFCF88D5C63E741503073F946BD5E9C39E1FB0AA09E0A7A0E590315D48F12385EAAA46CB9117CC1228D813BF9F8AACC6CCF1FC9BDAB29A4D67CAFF304AAE2CB019CE780451354C07"})
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
