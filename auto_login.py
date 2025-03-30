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
    browser.add_cookie({"name": "MUSIC_U", "value": "002565BF1BF5B672ACF3A4DC9CF311E4B7E59F3CF098ADF0F3958F66EEF3EC2DAB169DCBDC349AEBC91BE4F122819AC74A3A03A3E8BF7736983705B5BFEC9B2F0926207F889FD31785308613D8AE115179FAA60B0C6A575247AEDF2603F51A41B704C50B4BDC90489D4AF59F8FA1F5E7814F1240EB5CB52E58CDDAB2A3AB8317AFB0CFD33D2F62719A9A33D2021907053BB9D3038DC889BE07A98353E4746BFC0B09FC33DE87AA525D18FB0453FD84D2BADD6644BE692178A51E7CF0C7A306C09402EB578FAD3A93FC6F8BB49D8DB2D84EAC97337AF9677BBFDB25D272342F85187E76907FD1496003834DA9B0F966C43AF54E7038AF7F4C4869A4DD738FF34FE68EF742ADC57C4DE7633F89FBA8E08C2793ABAAFDF12F6D7F8D03C35CB44E8657534D93313191119C6254545F38C7414019E29CF2E4BBAC550810A859113B9A097CD410D22FC80F708A5BE6EE5932FF748917CD27A5EB3298259D1060F71B573988877210AD5CA2E488FE6C811AA84EEB"})
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
