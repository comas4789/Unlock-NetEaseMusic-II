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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B6C570B0F824FBF39BADF06D19F0355C4E15FEB9ABEA6CA7059CB5523B8AE8D82FBEDEECA59C1E84122039465C9BF116621D8587F96E4DCF4902F6687962D7EED7024CAD117D40B641D2DB30EB822B5580B8743339920C54707AB6326C0FB6FD1D9326DD827D94B063FB142821BCAF390607C27D137FE2C8DA4469B6BAC22686A2C644DD17216A71320A71EFF3CDE6A6DD609ECBC3380F240E040831D82816D21BF189060B232D2B18421B3C5EBC19721B7BC78D0F2124DD595280C151045CEE16F1B8F3CEE8B49BAB04740E1C96BCA5D181915AD3A6A8FBF0F3C457B000EBEB7830A3C5D6B551B6D7D6CB512C33467FECA46C2D3C57C7C9159935AD0CE8E24E952CF119D5E8E871BEC40CD4EADBC587A99615F7102E72D09BD2C3E955BEA0C1B653607C7B46D0ECA9A2A642290ADFF2B039010661432A2CE468AFE2659A23857F66CA5E29E7970BBDB0438D8859B1AE951FC0037DF943B4DA9FC5A3F466F1A8"})
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
