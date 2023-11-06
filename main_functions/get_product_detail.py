# import libraries
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math

# import custom helper functions
from utils.helpers import findActiveButtons, print_message


def getReviewDetail(dvr):
    print('MANTAIN REVIEW')

    time.sleep(60)
    detail_content = dvr.page_source
    detail_soup = BeautifulSoup(detail_content, 'html.parser')

    total_reviews_element = detail_soup.find('p', class_='css-e84n4s-unf-heading e1qvo2ff8')
    current_rows_of_reviewers = detail_soup.find_all('article', class_='css-72zbc4')
    print('current_rows_of_reviewers LENGTH', len(current_rows_of_reviewers))
    print('current_rows_x', current_rows_of_reviewers)
    if len(current_rows_of_reviewers) > 0:
        total_review_string = total_reviews_element.text
        total_review = total_review_string.split()[3] if total_review_string else None
        print('TOTAL_REVIEW', total_review)
        if total_review is not None:
            FIND_REVIEW_PAGE_CONTROLLER = detail_soup.find('div', class_='css-1xqkwi8')
            print('FIND_REVIEW_PAGE_CONTROLLER', FIND_REVIEW_PAGE_CONTROLLER)
            navigation_controller = ''
            if FIND_REVIEW_PAGE_CONTROLLER:
                navigation_controller = detail_soup.find('nav', class_='css-txlndr-unf-pagination')
            else:
                navigation_controller = None
            print('navigation_controller', navigation_controller)

            find_total_button_controller = navigation_controller.find_all('button', class_='css-bugrro-unf-pagination-item') if navigation_controller is not None else None
            find_total_button_controller_element = dvr.find_elements(By.XPATH, '//button[@class="css-bugrro-unf-pagination-item"]') if navigation_controller is not None else None
            print('find_total_button_controller_find_total_button_controller', find_total_button_controller[0] if navigation_controller is not None else 'kosong')
            print('FIND_TOTAL_BUTTON_PAGE', find_total_button_controller[-1].text if find_total_button_controller is not None else '')      
         
            current_active_button = None
            if find_total_button_controller is not None and find_total_button_controller_element is not None:
                current_active_button =  findActiveButtons(find_total_button_controller_element, 'data-active')
            else:
                current_active_button = None
                
            print('current_active_button', current_active_button)
            review_list = []
            review_count = 0
            review_count_per_page = 0
            REVIEW_PER_PAGE = 10
            
            while review_count < int(total_review):
                if current_active_button is not None:
                    while review_count_per_page < REVIEW_PER_PAGE:
                        for review in current_rows_of_reviewers:
                            customer_name = review.find('span', class_='name').text
                            customer_review_container = review.find('p', class_='css-ed1s1j-unf-heading e1qvo2ff8')
                            customer_review = customer_review_container.find('span').text

                            customer_review_item = {
                                'customer_name': customer_name,
                                'customer_review': customer_review
                            }
                            review_list.append(customer_review_item)
                            print('review_count_current_active_button', review_count)
                            review_count += 1
                            review_count_per_page += 1
                    else:
                        current_page = math.floor(review_count / REVIEW_PER_PAGE)
                        print('current_page', current_page)
                        button_controller_length = len(find_total_button_controller) if navigation_controller is not None else None
                        print('button_controller_length', button_controller_length)
                        print('find_controller_button', find_total_button_controller_element[current_page + 1 if current_page < button_controller_length else current_page] if navigation_controller is not None else None)
                        find_total_button_controller_element[current_page + 1 if current_page < button_controller_length else current_page].click() if navigation_controller is not None else None
                        review_count_per_page = 0
#                       Load element
                        time.sleep(30)
                else:
                    for review in current_rows_of_reviewers:
                        customer_name = review.find('span', class_='name').text
                        customer_review_container = review.find('p', class_='css-ed1s1j-unf-heading e1qvo2ff8')
                        customer_review = customer_review_container.find('span').text

                        customer_review_item = {
                            'customer_name': customer_name,
                            'customer_review': customer_review
                        }
                        review_list.append(customer_review_item)
                        print('review_count', review_count)
                        review_count += 1
        print_message(f'REVIEW - LIST {review_list}', 'info', True)
        return review_list
    else:
        return []


def getSellerDetail(dvr):
    wait = WebDriverWait(dvr, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1wbjdax')))
    detail_content = dvr.page_source
    detail_soup = BeautifulSoup(detail_content, 'html.parser')

    seller_container = detail_soup.find('div', class_='css-1wbjdax')
    seller_name = detail_soup.find('div', class_='css-k008qs')
    seller_image = detail_soup.find('img', class_='css-ebxddb')
    detail_soup = BeautifulSoup(detail_content, 'html.parser')
    seller_name = detail_soup.find('h2', class_='css-1wdzqxj-unf-heading e1qvo2ff2').text 
    seller_performance = detail_soup.find_all('div', class_='css-1h5fp8g')
    seller_responsiveness = seller_performance[1].find('span').text
    seller_rate = seller_performance[0].find('span').text
    seller_location_element = detail_soup.find('h2', class_='css-1pd07ge-unf-heading e1qvo2ff2')
    seller_location = seller_location_element.find('b').text
    seller_category = dvr.find_element(by=By.CLASS_NAME, value='css-ebxddb').get_attribute('alt')

    seler_section = {
        'seller_name' : seller_name,
        'seller_responsiveness': seller_responsiveness,
        'seller_rate': seller_rate,
        'seller_category': seller_category,
        'seller_location': seller_location
    }
    return seler_section

def getProductDetail(dvr):
    detail_content = dvr.page_source
    detail_soup = BeautifulSoup(detail_content, 'html.parser')
    time.sleep(10)
    PRODUCT_DETAIL = {}
    
    # PRODUCT SECTION
    product_name = detail_soup.find('h1', class_='css-1os9jjn').text
    product_category = detail_soup.find_all('li', class_='css-d5bnys')
    product_category_index = product_category[1].text
    
    product_price_container = detail_soup.find('div', class_='css-chstwd')
    product_original_price = product_price_container.find('div', class_='original-price').text if(product_price_container.find('div', class_='original-price')) else ''
    product_price = product_price_container.find('div', class_='price').text
    quantity_of_product_sold = detail_soup.find_all('p', class_='css-vni7t6-unf-heading e1qvo2ff8')[2] if  len(detail_soup.find_all('p', class_='css-vni7t6-unf-heading e1qvo2ff8')) else ''
    get_quanity_of_product_sold = quantity_of_product_sold.text if quantity_of_product_sold != '' else ''
    
    product_detail = {
        'product_name': product_name,
        'product_category_index': product_category_index,
        **({'product_original_price': product_original_price} if product_original_price else {}),
        'product_sold_quantity': get_quanity_of_product_sold if get_quanity_of_product_sold else '',
        'product_price': product_price
    }
    
    PRODUCT_DETAIL.update(product_detail)
    
    # SELLER SECTION
    
    scroll_height = 500
    dvr.execute_script(f"window.scrollBy(0, {scroll_height});")
    time.sleep(10)
    
    SELLER_DETAIL = getSellerDetail(dvr)


    # CUSTOMER REVIEW SECTION
    scroll_height2 = 1000
    dvr.execute_script(f"window.scrollBy(0, {scroll_height2});")
    
    REVIEW_DETAIL = getReviewDetail(dvr)


    statement = ''
    object_statement = {}

    for index, item in enumerate(REVIEW_DETAIL):
        print(index)
        if index == 0:
            SELLER_DETAIL.update(item)
        else:
            object_statement = item
            
    product_detail_merged =  f'{statement}, {object_statement}' if object_statement and len(REVIEW_DETAIL) > 0 else statement
    
    # update seller section
    PRODUCT_DETAIL.update(SELLER_DETAIL)
    
    #update customer section
    PRODUCT_DETAIL['customer'] = product_detail_merged if len(REVIEW_DETAIL) > 0 else "'customer_name': '', 'customer_review': ''"
 
    
    ## PRODUCT DETAIL DONE GO BACK
    print_message(f'PRODUCT_DETAIL_SECTION {PRODUCT_DETAIL}', 'info', True )
    return PRODUCT_DETAIL