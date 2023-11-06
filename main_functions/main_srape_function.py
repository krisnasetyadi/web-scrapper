from utils.helpers import print_message
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# F U N C T I O N S

from main_functions.config_parameters import BASE_SEARCH_URL_PARAMETER, PROXY_SERVER
from utils.helpers import scrollFromToptoBottom
from main_functions.get_product_detail import getProductDetail

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
    time.sleep(30)
    print_message(f'REQUESTING_URL . . . {requestURL}', 'info')

    wait = WebDriverWait(driver, 60)
    all_item_each_page = [driver.find_element(By.XPATH, '//div[@class="css-llwpbs"]')]
    total_item_per_page = len(all_item_each_page)
    print('each_item LENGTH', total_item_per_page )
    LIST_OF_PRODUCT = []
    for item in all_item_each_page:
        print('item', item)
        anchor = item.find_element(By.TAG_NAME, 'a')
        current_url = driver.current_url
        anchor.click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-856ghu"]')))
        
        new_url = driver.current_url
        print('new_url', new_url)
        if current_url != new_url:
            [is_scrolled]=scrollFromToptoBottom(driver, 'pdp_comp-discussion_faq', True)
            get_product_detail = getProductDetail(driver)
            LIST_OF_PRODUCT.append(get_product_detail['product'])
            LIST_OF_PRODUCT.append(get_product_detail['seller'])
            LIST_OF_PRODUCT.append(get_product_detail['customer'])
            driver.back()
            print('back?')
    print_message(f'main function {LIST_OF_PRODUCT}', 'info', True)
    print('len(LIST_OF_PRODUCT)', len(LIST_OF_PRODUCT))
    if len(LIST_OF_PRODUCT) > 0:
        df = pd.DataFrame(LIST_OF_PRODUCT)
        
        df.index += 1
        df.index.rename('number', inplace=True)
        df.to_csv('product.csv')
        
        print('DONE')