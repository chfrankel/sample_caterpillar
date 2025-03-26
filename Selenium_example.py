# © 2025 Charles Frankel. All rights reserved.

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

script_directory = os.path.dirname(os.path.abspath(__file__))

################################################################################################################
# WebDriver class
# 
# PURPOSE:
#   restricted to interacting with the web driver. Getting pages, clicking links, going back
#   does now have knowledge of the specific pages it is navigating to - i.e. what links to look for
#
################################################################################################################
class WebDriver:
    # class-wide variables
    # CHROME_DRIVER_PATH = "/home/adams_st/-linux64/chromedriver"
    CHROME_DRIVER_PATH = f"{script_directory}/Chromium/chromedriver-mac-arm64/chromedriver"
    #"/Users/charlesfrankel/Desktop/Pat/Pat_Chromium/chromedriver-mac-arm64/chromedriver"
    # CHROME_DRIVER_PATH = "./chromedriver"
    SLEEP_TIME_BETWEEN_PAGES = 0

    def __init__(self, run_headless = True) -> None:
        self.SLEEP_TIME_BETWEEN_PAGES = WebDriver.SLEEP_TIME_BETWEEN_PAGES
        options = Options()
        if (run_headless):
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usageu')
        service = Service(WebDriver.CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        self.driver = driver
    
    def __del__(self):
        self.driver.quit()
    
    def get_page(self, url, wait_path = None, sleep_time = None) -> bool:
        if not sleep_time:
            sleep_time = self.SLEEP_TIME_BETWEEN_PAGES

        try:
            self.driver.get(url)
        except Exception as e:
            time.sleep(sleep_time)
            try:
                self.driver.get(url)
            except Exception as e:
                return False # tried to download this twice and it failed

        if wait_path:
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, wait_path)))
            except Exception as e:
                pass

        time.sleep(sleep_time)

        return True

    def go_back(self, back_count:int = 1):
        for i in range(back_count):
            self.driver.back()
            time.sleep(self.SLEEP_TIME_BETWEEN_PAGES)

    def click_link(self, link):
        try:
            link.click()
            time.sleep(self.SLEEP_TIME_BETWEEN_PAGES)
        except Exception as e:
            link.click()
            print(f"Error clicking: {e}, retrying")
            time.sleep(self.SLEEP_TIME_BETWEEN_PAGES)

    def click_link_if_present(self, link_ref): # a "display all links"
            try:
                found_link = self.driver.find_element(By.CSS_SELECTOR, link_ref)
                if found_link:
                    self.click_link(found_link)
            except Exception as e:
                pass #ignore exceptions
    
    def load_links(self) -> list[any]:
        # Fetch all links and their text using JavaScript
        script = """
        let links = document.getElementsByTagName('a');
        let result = [];
        for (let link of links) {
            result.push({text: link.textContent.toLowerCase(), href: link.href});
        }
        return result;
        """
        self.cached_links = self.execute_script(script)
        return self.cached_links
    
    def find_unique_hrefs(self, tag_name, inner_tag_name, href_prefix):
        tag_section = self.driver.find_elements(By.TAG_NAME, tag_name)
        links = []
        for tag in tag_section: # could be multiple tag_name sections
            links += tag.find_elements(By.TAG_NAME, inner_tag_name)

        valid_links = [link for link in links if link.get_attribute('href').lower().startswith(href_prefix)]
        return self.unique_links(valid_links)
    
    def unique_links(self, links):
        unique_links = {link.get_attribute("href") : link for link in links}
        return [i for i in unique_links.values()]
        
    def find_element(self, selector, element):
        try:
            return self.driver.find_element(selector, element)
        except Exception as e:
            return None

    def find_elements(self, selector, element):
        return self.driver.find_elements(selector, element)
    
    def execute_script(self, JavaScript_text, parameter = None):
        if parameter:
            return self.driver.execute_script(JavaScript_text, parameter) # allow the selenium driver to interpret the parameter
        else:
            return self.driver.execute_script(JavaScript_text)
    
    def find_xpath(self, xpath_list) -> list:
        for xpath in xpath_list:
            try:
                found_items = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, xpath))
                )
                return found_items
            except Exception as e:
                pass
        return []

################
# MAIN entrypoint
################
if __name__ == "__main__":
    print("No main in WebDriver.py")
