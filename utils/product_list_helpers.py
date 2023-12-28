from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import time
import sys

from utils.helpers import extractHrefParameter
from utils.helpers import print_message, scrollFromToptoBottom, saveToCSV, storingLoggingAs
from main_functions.product_detail.get_main_product_detail import getProductDetail

def getAllURLPerPage(driver):
    redirect_urls = []
    wait = WebDriverWait(driver, 120)
    
    # css-19oqosi for search 
    # for category class css-bk6tzz e1nlzfl2
    all_item_each_page = driver.find_elements(By.XPATH, '//div[@class="css-bk6tzz e1nlzfl2"]')
    total_item_per_page = len(all_item_each_page)
    storingLoggingAs('info', f'total item per page: {total_item_per_page}')

    for item_index in range(int(total_item_per_page)):
        list_item_each_page = driver.find_elements(By.XPATH, '//div[@class="css-bk6tzz e1nlzfl2"]')
        item = list_item_each_page[item_index]
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        anchor = item.find_element(By.TAG_NAME, 'a')
        href = anchor.get_attribute('href')
        url = extractHrefParameter(href)
        redirect_urls.append(url)
    return redirect_urls

def openNewTabWindow(driver, url, listProducts=[], keyword='', index_item=0, total_item=0):
    max_size_threshold = 10 * 1024 * 1024  # 10 MB
    driver.execute_script("window.open('', '_blank');")
    # Switch to the new tab
    
    driver.switch_to.window(driver.window_handles[-1])
    storingLoggingAs('info', f'navigating to {url}' )

    # Navigate to the URL in the new tab
    driver.get(url)
    print('sleep for 60 seconds')
    time.sleep(60)
    
    print('scrolling to detail footer...')
    [scrolled] = scrollFromToptoBottom(driver, 'pdp_comp-discussion_faq', False, False, 5)

    print(f'scrolled finished: {scrolled}. trying to collect product detail')
    try:
        get_product_detail = getProductDetail(driver)

        listProducts.append(get_product_detail)
        storingLoggingAs('info', f'listProducts {listProducts}')
        current_size = sys.getsizeof(listProducts)
        storingLoggingAs('warning', f'current_size_of_product_list_variable: {current_size}')
        time.sleep(30)
        saveToCSV([get_product_detail], keyword, 'success_each_item', 'each_product')
        storingLoggingAs('info', f'successfully saved in each products folder {index_item} of {total_item}')
        print_message(f'successfully saved in each products folder', 'success', True)
    except WebDriverException as e:
        if(len(listProducts) > 0):
            saveToCSV(listProducts, keyword, 'failed', 'action_failed')
            storingLoggingAs('error', f'listProducts_error {listProducts}')
            print_message(f'WebDriverException: {e}', 'danger', True)

    # Close the new tab
    driver.close()

    # Switch back to the original tab
    driver.switch_to.window(driver.window_handles[0])


def getTotalPagination (driver):
    MAX_NAVIGATION_BUTTON = 11
    NAV_CONTAINER_CLASS = 'css-txlndr-unf-pagination'

    nav_pagination_container = driver.find_element(By.XPATH, f'//nav[@class="{NAV_CONTAINER_CLASS}"]') if driver.find_elements(By.XPATH, f'//nav[@class="{NAV_CONTAINER_CLASS}"]') else None
    nav_button_element = nav_pagination_container.find_elements(By.TAG_NAME, 'li') if nav_pagination_container is not None else []
    last_pagination_button = nav_button_element[MAX_NAVIGATION_BUTTON - 2].text if len(nav_button_element) == MAX_NAVIGATION_BUTTON  else nav_button_element[len(nav_button_element) - 2].text
    return last_pagination_button

