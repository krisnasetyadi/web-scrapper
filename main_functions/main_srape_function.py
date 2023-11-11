import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
# F U N C T I O N S
from utils.helpers import print_message, scrollFromToptoBottom
from main_functions.config_parameters import BASE_SEARCH_URL_PARAMETER, PROXY_SERVER
from main_functions.get_product_detail import getProductDetail
from utils.product_helpers import iterateProductPerPage

MAX_RETRY = 10

def scrapeTokopediaData(urls = []):
    print_message(f'SCRAPE FUNCTION RUNNING ON PROXY {PROXY_SERVER} . . .', 'success', bold=True)
    chrome_options = webdriver.ChromeOptions()
    services = Service('chromedriver.exe')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')
    chrome_options.add_argument('--proxy-server={}'. format(PROXY_SERVER))
    print_message(f'ARGUMENT_ADDED', 'info')
    time.sleep(10)
    driver = webdriver.Chrome(service=services, options=chrome_options)
    print_message(f'DRIVER_SETUP', 'info')
    requestURL = driver.get(BASE_SEARCH_URL_PARAMETER)
    content = driver.page_source
    list_content_soup = BeautifulSoup(content, 'html.parser')
    find_error_el = list_content_soup.find('body', class_='neterror')

    if find_error_el is None:
        time.sleep(60)
        scrollFromToptoBottom(driver, 'css-70qvj9', False, True, 10)

        iterateProductPerPage(driver, WebDriverWait(driver, 60))
        wait = WebDriverWait(driver, 60)
        # css-llwpbs
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="prd_container-card"]')))
        all_item_each_page = driver.find_elements(By.XPATH, '//div[@class="prd_container-card"]')
        total_item_per_page = len(all_item_each_page)

        LIST_OF_PRODUCT = []
        item_counter_page = 0
        detail_urls_per_page = []
           
        while item_counter_page < total_item_per_page:
            for item_index in range(total_item_per_page):
                print('item_counter_page', item_counter_page)
                list_item_each_page = driver.find_elements(By.XPATH, '//div[@class="prd_container-card"]')
                item = list_item_each_page[item_index]
                print('item', item)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
                anchor = item.find_element(By.TAG_NAME, 'a')
     
                print('achorrr', anchor)
                href = anchor.get_attribute('href')
                print('HREF', href)
                current_url = driver.current_url
                print('current_url', current_url)
                anchor.click()

                wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-856ghu"]')))
                
                new_url = driver.current_url
                print('new_url', new_url)
                if current_url != new_url:
                    time.sleep(60)
                    detail_urls_per_page.append(new_url)
                    [is_scrolled]=scrollFromToptoBottom(driver, 'pdp_comp-discussion_faq', True)
                    get_product_detail = getProductDetail(driver)
                    print('GET_PRODUCT_DETAIL', get_product_detail)
                    LIST_OF_PRODUCT.append(get_product_detail)
                    item_counter_page =+ 1
                    ## WHEN GET PRODUCT DETAIL DONE IT'LL GO BACK TO PRODUCT LIST ##
                    driver.back()
                    print('BACK SUCCEED')
                    time.sleep(30)
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-llwpbs"]')))
            print('detail_urls_per_pagess', detail_urls_per_page)
            print_message(f'main function {LIST_OF_PRODUCT}', 'info', True)
            print('len(LIST_OF_PRODUCT)', len(LIST_OF_PRODUCT))
            if len(LIST_OF_PRODUCT) > 0:
                df = pd.DataFrame(LIST_OF_PRODUCT)
                df.index += 1
                df.index.rename('number', inplace=True)
                df.to_csv('product.csv')

                print_message('DATAFRAME SUCESSFULLY SAVED ON CSV', 'info', True)
    else:
        raise(NoSuchElementException)
    # error_page = True if driver.find_element(By.XPATH, '//body[@class="neterror"]') else False
    # print('error_page', error_page)
    # elif error_page:
    #     print_message('Something error', 'danger')
    #     raise(NoSuchElementException)
  
