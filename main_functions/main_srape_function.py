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
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

# F U N C T I O N S
from utils.helpers import print_message, scrollFromToptoBottom, saveToCSV, storingLoggingAs, playSoundWithStatus, extractCurrentUrlPage
from config.config_parameters import BASE_SEARCH_URL_PARAMETER, PROXY_SERVER, KEYWORD

from utils.product_list_helpers import getAllURLPerPage, openNewTabWindow

MAX_RETRY = 10

def scrapeTokopediaData(url_with_pagination=''):

    print_message(f'SCRAPE FUNCTION RUNNING ON PROXY {PROXY_SERVER} . . .', 'success', bold=True)
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = PROXY_SERVER
    proxy.ssl_proxy = PROXY_SERVER
    ua = UserAgent()
    
    uc_chrome_options = uc.ChromeOptions()
    uc_chrome_options.add_argument(f'user-agent={ua.random}')
    uc_chrome_options.add_argument('--disable-popup-blocking')

    print_message(f'http: {proxy.http_proxy}, ssl: {proxy.ssl_proxy}', 'info', True)

    print_message('argument added', 'info')
    time.sleep(10)
    driver = uc.Chrome(options=uc_chrome_options, use_subprocess=False)
    
    print_message(f'setting up driver . . .', 'info')

    driver.get(url_with_pagination)
    content = driver.page_source
    list_content_soup = BeautifulSoup(content, 'html.parser')
    find_error_el = list_content_soup.find('body', class_='neterror')

    LIST_OF_PRODUCT = []
    if find_error_el is None:
        try:
            time.sleep(40)
            print('running without driver error')
            FOOTER_CLASS = 'css-dmrkw7'
            CONTAINER_PRODUCT_CARD_DIV = 'css-1xpribl e1nlzfl3'
            PRODUCT_CARD_DIV_CLASS = 'css-bk6tzz e1nlzfl2'
            PRODUCT_NOT_FOUND_DIV_CLASS = 'css-rsd0q9'
            MAX_EXPECTED_PAGINATION = 100
            storingLoggingAs('info', 'running without driver error')
            [scrolled] = scrollFromToptoBottom(driver, f'{FOOTER_CLASS}', False, True, 10)
            print('scrolled to footer', scrolled)
            wait = WebDriverWait(driver, 120)
            
            # 'css-llwpbs' class that containt prd_container-card or css-19oqosi (search)
            # css-1xpribl e1nlzfl3 class that contain css-bk6tzz e1nlzfl2 (category)
            wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@class="{CONTAINER_PRODUCT_CARD_DIV}"]')))
            print('waiting done')

            # product tidak ditemukan container div class PRODUCT_NOT_FOUND_DIV_CLASS    
            
            # print_message(f'get_total_pagination {int(total_pagination)}', 'info' )

            # note pagination
            #  - click the next element
            #  - driver get (get_default) query by add query = 
            # css-19oqosi for search 
            # for category class css-bk6tzz e1nlzfl2
            current_pagination = 0

            all_item_each_page = driver.find_elements(By.XPATH, f'//div[@class="{PRODUCT_CARD_DIV_CLASS}"]')

            total_item_per_page = len(all_item_each_page)

            urls = getAllURLPerPage(driver)
            page_number = extractCurrentUrlPage(url_with_pagination)
            print('IS_SAME_LENGTH', len(urls), total_item_per_page)
            if len(urls) == total_item_per_page:
                item_counter_page = 0
                # current_url = driver.current_url
                for url_index, url in enumerate(urls):
                    time.sleep(10)
                    storingLoggingAs('info', f'processing {url_index} of {len(urls)} url in page {current_pagination}. opening new tab...')

                    openNewTabWindow(driver, url, LIST_OF_PRODUCT, KEYWORD, url_index, total_item_per_page, page_number)
                    item_counter_page += 1
                    time.sleep(10)                   
                print('item_counter_page', item_counter_page)
                if len(LIST_OF_PRODUCT) > 0:
                    saveToCSV(LIST_OF_PRODUCT, KEYWORD, 'success', f'page:{page_number}')
                    
                    print_message('DATAFRAME EACH PAGE SUCESSFULLY SAVED ON CSV', 'info', True)
                    driver.close()
                    current_pagination += 1

        except WebDriverException as e:
            playSoundWithStatus('error', 4)
            if "ERR_HTTP2_PROTOCOL_ERROR" in str(e):
                print_message(f'Encountered ERR_HTTP2_PROTOCOL_ERROR: {e}', 'error', True)
                if len(LIST_OF_PRODUCT) > 0:
                    saveToCSV(LIST_OF_PRODUCT, KEYWORD, 'failed', f'http2_protocol_errorf_page:{page_number}')
                    print_message('FAILED 2 DATAFRAME SUCESSFULLY SAVED ON CSV', 'info', True)

                
