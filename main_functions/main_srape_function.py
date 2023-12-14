import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
# F U N C T I O N S
from utils.helpers import print_message, scrollFromToptoBottom,saveToCSV
from main_functions.config_parameters import BASE_SEARCH_URL_PARAMETER, PROXY_SERVER, KEYWORD
from main_functions.get_product_detail import getProductDetail
from utils.product_list_helpers import getAllURLPerPage

MAX_RETRY = 10

def scrapeTokopediaData(urls = []):
    print_message(f'SCRAPE FUNCTION RUNNING ON PROXY {PROXY_SERVER} . . .', 'success', bold=True)
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = PROXY_SERVER
    proxy.ssl_proxy = PROXY_SERVER
    ua = UserAgent()
    chrome_options = webdriver.ChromeOptions()
    services = Service('chromedriver.exe')
    chrome_options.add_argument(f'user-agent={ua.random}')
    # chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')
    # chrome_options.add_argument(f'--proxy-server=http://{proxy.http_proxy}')
    # chrome_options.add_argument(f'--proxy-server=https://{proxy.ssl_proxy}')
    print_message(f'http: {proxy.http_proxy}, ssl: {proxy.ssl_proxy}', 'info', True)

    print_message('argument added', 'info')
    time.sleep(10)
    driver = webdriver.Chrome(service=services, options=chrome_options)
    print_message(f'setting up driver . . .', 'info')

    driver.get(BASE_SEARCH_URL_PARAMETER)
    content = driver.page_source
    list_content_soup = BeautifulSoup(content, 'html.parser')
    find_error_el = list_content_soup.find('body', class_='neterror')

    LIST_OF_PRODUCT = []
    if find_error_el is None:
        try:
            time.sleep(60)
            print('running without driver error')
            [scrolled] = scrollFromToptoBottom(driver, 'css-dmrkw7', False, True, 10)
            print('scrolled', scrolled)
            wait = WebDriverWait(driver, 120)
            
            # 'css-llwpbs' class that containt prd_container-card or css-19oqosi
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-llwpbs"]')))
            print('waiting done')

            all_item_each_page = driver.find_elements(By.XPATH, '//div[@class="css-19oqosi"]')

            total_item_per_page = len(all_item_each_page)

        
            urls = getAllURLPerPage(driver)
          
            print('IS_SAME_LENGTH', len(urls), total_item_per_page)
            if len(urls) == total_item_per_page:
                item_counter_page = 0
                current_url = driver.current_url
                for url in urls:
                    driver.get(url)
                    time.sleep(10)
                    new_url = driver.current_url
                    time.sleep(10)
                   
                    if current_url != new_url:
                        time.sleep(60)
                        print('scrolling . . .')
                        [scrolled] = scrollFromToptoBottom(driver, 'pdp_comp-discussion_faq', False, True, 10)

                        print(f'scrolled finished: {scrolled}. trying to collect product detail')
                        try:
                            get_product_detail = getProductDetail(driver)
                            print('GET_PRODUCT_DETAIL', get_product_detail)
                            LIST_OF_PRODUCT.append(get_product_detail)
                            item_counter_page =+ 1

                            ## WHEN GET PRODUCT DETAIL DONE IT'LL GO BACK TO PRODUCT LIST ##
                            driver.back()
                            print('BACK SUCCEED')
                            time.sleep(30)
                            print_message(f'CURRENT_LIST_OF_PRODUCT: => {LIST_OF_PRODUCT}', 'success', True )
                            current_url_after_back = driver.current_url
                            print('current_url_after_back', current_url_after_back)
                            driver.delete_all_cookies()
                            time.sleep(5)
                            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-llwpbs"]')))
                        except WebDriverException as e:
                            if(len(LIST_OF_PRODUCT) > 0):
                                saveToCSV(LIST_OF_PRODUCT, KEYWORD, 'failed', 'action_failed')
                                print_message(f'WebDriverException: {e}', 'danger', True)

                print('item_counter_page =+ 1', item_counter_page)
                if len(LIST_OF_PRODUCT) > 0:
                    saveToCSV(LIST_OF_PRODUCT, KEYWORD, 'success')
                    print_message('DATAFRAME SUCESSFULLY SAVED ON CSV', 'info', True)

        except WebDriverException as e:
            if "ERR_HTTP2_PROTOCOL_ERROR" in str(e):
                print_message(f'Encountered ERR_HTTP2_PROTOCOL_ERROR: {e}', 'error', True)
                if len(LIST_OF_PRODUCT) > 0:
                    saveToCSV(LIST_OF_PRODUCT, KEYWORD, 'failed', 'http2_protocol_error')
                    print_message('FAILED 2 DATAFRAME SUCESSFULLY SAVED ON CSV', 'info', True)

                
