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
from utils.helpers import print_message, scrollFromToptoBottom
from main_functions.config_parameters import BASE_SEARCH_URL_PARAMETER, PROXY_SERVER, KEYWORD
from main_functions.get_product_detail import getProductDetail

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

    current_datetime = datetime.now()
    formatted_timestamp = current_datetime.strftime("%Y%m%d%H%M%S")
    print('formatted timestamp set up')
    print('formatted_timestamp', formatted_timestamp)
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
            # prd_container-card class not working anymore ?
            # driver.find_elements(By.XPATH, '//div[@class="prd_container-card"]')

            all_item_each_page = driver.find_elements(By.XPATH, '//div[@class="css-19oqosi"]')

            total_item_per_page = len(all_item_each_page)

            item_counter_page = 0
            detail_urls_per_page = []
            print('total_item_per_page', total_item_per_page)
            while item_counter_page < total_item_per_page:
                for item_index in range(total_item_per_page):
                    print('item_counter_page', item_counter_page)


                    list_item_each_page = driver.find_elements(By.XPATH, '//div[@class="css-19oqosi"]')
                    item = list_item_each_page[item_index]
                    print('reading item . . .')
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
                    anchor = item.find_element(By.TAG_NAME, 'a')
        
                    print('reading anchor . . .', anchor)

                    href = anchor.get_attribute('href')
                    print('getting href', href)

                    # note : different approach get href 
                    # then call this func driver.get(href) *what would it get* 
                    # this approach not recommended

                    # note : move_to_element move_to_element_with_offset

                    # note : differet approach execute by javascript
                    # then call driver.execute_script("arguments[0].click();", anchor)
                    # getting this ERR_HTTP2_PROTOCOL_ERROR and cannot back url 

                    current_url = driver.current_url
                    print('current url before click actions', current_url)

                    # actions = ActionChains(driver)
                    # actions.move_to_element(anchor)

                    time.sleep(5)
                    # actions.click()

                    # actions.perform()
                    try:
                        anchor.click()
                        print('is_clicked')
                    except WebDriverException as e:
                        if(len(LIST_OF_PRODUCT) > 0):
                            storing = []
                            for i in LIST_OF_PRODUCT:
                                storing.extend(i)
                            print('LIST_OF_PRODUCT_FAILED', LIST_OF_PRODUCT)
                            print('storing_WebDriverException', storing)
                            df = pd.DataFrame(storing)
                            df.index += 1
                            df.index.rename('number', inplace=True)
                            df.to_csv(f'product_{KEYWORD}_action_click_element_failed_{formatted_timestamp}.csv')
                            if "element click intercepted" in str(e):
                                actions = ActionChains(driver)
                                actions.move_to_element(anchor).click().perform()
                                # Handle the intercepted click exception here, for example, print a message
                                print("Element click intercepted. Moving on to the next iteration.")
                            if "ERR_HTTP2_PROTOCOL_ERROR" in str(e):
                                print_message(f'Encountered ERR_HTTP2_PROTOCOL_ERROR: {e}', 'danger', True)
                            else:
                            # Handle other WebDriverException or print the exception for debugging
                                print_message(f'WebDriverException: {e}', 'danger', True)




                    content = driver.page_source
                    list_content_soup = BeautifulSoup(content, 'html.parser')
                    element_click_get_error = list_content_soup.find('body', class_='neterror')
                    
                    # max_retry_click = 5
                    # retry_count_click = 0
                    # while element_click_get_error and retry_count_click < max_retry_click:
                    #     print(f'retrying click {retry_count_click} / {max_retry_click} to timeout')
                    #     list_item_each_page = driver.find_elements(By.XPATH, '//div[@class="css-19oqosi"]')
                    #     item = list_item_each_page[item_index]
                    #     print('reading item . . .')
                    #     wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
                    #     anchor = item.find_element(By.TAG_NAME, 'a')
            
                    #     print('reading anchor . . .', anchor)

                    #     href = anchor.get_attribute('href')
                    #     print('getting href', href)

                    #     # note : different approach get href 
                    #     # then call this func driver.get(href) *what would it get* 
                    #     # this approach not recommended

                    #     # note : move_to_element move_to_element_with_offset

                    #     # note : differet approach execute by javascript
                    #     # then call driver.execute_script("arguments[0].click();", anchor)
                    #     # getting this ERR_HTTP2_PROTOCOL_ERROR and cannot back url 

                    #     current_url = driver.current_url
                    #     print('current url before click actions', current_url)

                    #     # actions = ActionChains(driver)
                    #     # actions.move_to_element(anchor)

                    #     time.sleep(5)
                    #     # actions.click()

                    #     # actions.perform()
                    #     anchor.click()
                    #     retry_count_click += 1
                    # retry_count_click = 0


                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-856ghu"]')))
                    
                    new_url = driver.current_url
                    print('new_url after click action', new_url)
                    if current_url != new_url:
                        time.sleep(60)
                        detail_urls_per_page.append(new_url)
                        [is_scrolled]=scrollFromToptoBottom(driver, 'pdp_comp-discussion_faq', True)

                        print(f'scrolled finished: {is_scrolled}. trying to collect product detail')

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
                print('detail_urls_per_pagess', detail_urls_per_page)
                print_message(f'main function {LIST_OF_PRODUCT}', 'info', True)
                print('len(LIST_OF_PRODUCT)', len(LIST_OF_PRODUCT))
                if len(LIST_OF_PRODUCT) > 0:
                    df = pd.DataFrame(LIST_OF_PRODUCT)
                    df.index += 1
                    df.index.rename('number', inplace=True)
                    df.to_csv(f'product_{KEYWORD}_{formatted_timestamp}.csv')

                    print_message('DATAFRAME SUCESSFULLY SAVED ON CSV', 'info', True)
            else:
                print_message('FAILED', LIST_OF_PRODUCT)
                print('len(LIST_OF_PRODUCT)', len(LIST_OF_PRODUCT))
                if len(LIST_OF_PRODUCT) > 0:
                    df = pd.DataFrame(LIST_OF_PRODUCT)
                    df.index += 1
                    df.index.rename('number', inplace=True)
                    df.to_csv(f'product_{KEYWORD}_failed_{formatted_timestamp}.csv')

                    print_message('FAILED 1 DATAFRAME SUCESSFULLY SAVED ON CSV', 'info', True)
                raise(NoSuchElementException)
        except WebDriverException as e:
            if "ERR_HTTP2_PROTOCOL_ERROR" in str(e):
                print_message(f'Encountered ERR_HTTP2_PROTOCOL_ERROR: {e}', 'error', True)
                if len(LIST_OF_PRODUCT) > 0:
                    df = pd.DataFrame(LIST_OF_PRODUCT)
                    df.index += 1
                    df.index.rename('number', inplace=True)
                    df.to_csv(f'product_{KEYWORD}_failed_{formatted_timestamp}.csv')

                    print_message('FAILED 2 DATAFRAME SUCESSFULLY SAVED ON CSV', 'info', True)

                
