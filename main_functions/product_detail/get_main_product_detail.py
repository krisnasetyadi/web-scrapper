# import libraries
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from utils.helpers import print_message, scrollFromToptoBottom, storingLoggingAs, flattenCustomerReviews
from main_functions.product_detail.get_seller_detail import getSellerDetail
from main_functions.product_detail.get_reviews_detail import getReviewDetail

def getProductDetail(driver):
    detail_content = driver.page_source
    detail_soup = BeautifulSoup(detail_content, 'html.parser')

    time.sleep(10)
    PRODUCT_DETAIL = {}
    wait = WebDriverWait(driver, 30)

    product_name = detail_soup.find('h1', class_='css-1os9jjn').text
    product_category = detail_soup.find_all('li', class_='css-d5bnys')
    product_category_index = product_category[1].text
    
    product_price_container = detail_soup.find('div', class_='css-chstwd')
    product_original_price = product_price_container.find('div', class_='original-price').text if(product_price_container.find('div', class_='original-price')) else ''
    product_price = product_price_container.find('div', class_='price').text
    
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-bczdt6')))
    quantity_of_sold_product_container = detail_soup.find('div', class_='css-bczdt6')
    quantity_of_product_sold = quantity_of_sold_product_container.find('p', class_='css-vni7t6-unf-heading e1qvo2ff8')
    get_quanity_of_product_sold = quantity_of_product_sold.text if quantity_of_product_sold else ''
    
    product_detail = {
        'product_name': product_name,
        'product_category_index': product_category_index,
        'product_sold_quantity': get_quanity_of_product_sold if get_quanity_of_product_sold else '',
        'product_price': product_price,
        'product_original_price': product_original_price if product_original_price else ''
    }

    # UPDATE PRODUCT SECTION #
    print('product detail collected')
    PRODUCT_DETAIL.update(product_detail)

    # SELLER SECTION #
    scroll_height = 500
    driver.execute_script(f"window.scrollBy(0, {scroll_height});")
    print('scrolled to seller sections')
    time.sleep(10)
    SELLER_DETAIL = getSellerDetail(driver)
    
    # UPDATE SELLER SECTION #
    print('seller detail collected')
    PRODUCT_DETAIL.update(SELLER_DETAIL)

    # CUSTOMER REVIEW SECTION #
    scroll_height2 = 1000
    driver.execute_script(f"window.scrollBy(0, {scroll_height2});")
    [scrolled] = scrollFromToptoBottom(driver, 'css-a21zsk', False, True, 10)
    print('scrolled to review sections', scrolled)

    REVIEW_DETAIL = getReviewDetail(driver)

    # UPDATE-REVIEW_DETAIL-SECTION #

    # logging.info(f'PRODUCT_DETAIL_LIEADT {PRODUCT_DETAIL}')
    storingLoggingAs('info', 'review detail collected successfully')
    print('review detail collected')

    PRODUCT_DETAIL_RESULT = {}
    if REVIEW_DETAIL is not None and len(REVIEW_DETAIL) > 0:
        PRODUCT_DETAIL['customer_reviews'] = REVIEW_DETAIL
        PRODUCT_DETAIL_RESULT['result'] = flattenCustomerReviews(PRODUCT_DETAIL, 'customer_reviews', 'customer_name', 'customer_review')
    else:
        PRODUCT_DETAIL.update({'customer_name': '', 'customer_review': ''})
    # logging.info(f"PRODUCT_DETAIL_RESULT{PRODUCT_DETAIL_RESULT['result'] if PRODUCT_DETAIL_RESULT else PRODUCT_DETAIL}")
    return PRODUCT_DETAIL_RESULT['result'] if PRODUCT_DETAIL_RESULT else PRODUCT_DETAIL