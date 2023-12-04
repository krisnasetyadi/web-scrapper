# import libraries
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math

# import custom helper functions
from utils.helpers import findActiveButtons, print_message, flattenCustomerReviews


def getReviewDetail(driver):
    print('MANTAIN REVIEW')

    time.sleep(60)
    detail_content = driver.page_source
    detail_soup = BeautifulSoup(detail_content, 'html.parser')

    total_reviews_element = detail_soup.find('p', class_='css-e84n4s-unf-heading e1qvo2ff8')
    current_rows_of_reviewers = detail_soup.find_all('article', class_='css-72zbc4')
    total_rows_per_page = len(current_rows_of_reviewers)
    print('total_rows_per_page', total_rows_per_page)
    print('current_rows_x', current_rows_of_reviewers)

    MAX_BUTTON_PER_NAV = 9

    # there's some reviews
    if len(current_rows_of_reviewers) > 0:
        review_list = []

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

            if navigation_controller is not None:
                # has pagination
                nav_button_container = driver.find_element(By.XPATH, '//div[@class="css-1xqkwi8"]')
                nav_button_element = nav_button_container.find_elements(By.XPATH, '//button[@class="css-bugrro-unf-pagination-item"]')
                last_pagination_button = nav_button_element[MAX_BUTTON_PER_NAV - 1].text if len(nav_button_element) == MAX_BUTTON_PER_NAV  else nav_button_element[len(nav_button_element) - 1].text
                
                for i in range(int(last_pagination_button)):
                    with_pagination_review_count = 0
                    with_pagination_review_count_per_page = 0
             
                    current_active_button = findActiveButtons(nav_button_element, 'data-active')
                  
                    print('current_active_button', current_active_button)

                    for review in current_rows_of_reviewers:
                        customer_name = review.find('span', class_='name').text
                        customer_review_container = review.find('p', class_='css-ed1s1j-unf-heading e1qvo2ff8')
                        customer_review = customer_review_container.find('span').text if customer_review_container else ''

                        customer_review_item = {
                            'customer_name': customer_name,
                            'customer_review': customer_review
                        }

                        review_list.append(customer_review_item)
                        with_pagination_review_count += 1
                        with_pagination_review_count_per_page += 1
                    print('iteration_with_pagination', i)
                    if with_pagination_review_count_per_page == len(current_rows_of_reviewers):

                        # why CLASS_NAME "css-bugrro-unf-pagination-item" declare twice ? to always refresh /fetch the element
                        nav_button_container_second = driver.find_element(By.XPATH, '//div[@class="css-1xqkwi8"]')
                        
                        next_element = nav_button_container_second.find_elements(By.XPATH, '//button[@class="css-16uzo3v-unf-pagination-item"]')[1]
                        next_element_aria_label = next_element.get_attribute('aria-label')
                        next_element_is_disabled = next_element.get_attribute('disabled')

                        if next_element_is_disabled:
                            print(f'next_element_is_disabled: finished reviewed {review_list}')
                            return review_list
                        elif next_element_aria_label == 'Laman berikutnya' and not next_element_is_disabled:
                            next_element.click()

                            # reset the value and click
                            with_pagination_review_count_per_page = 0

                            time.sleep(5)
                            # Fetch the new set of current_rows_of_reviewers
                            
                            detail_content = driver.page_source
                            detail_soup_second = BeautifulSoup(detail_content, 'html.parser')

                            current_rows_of_reviewers = detail_soup_second.find_all('article', class_='css-72zbc4')
                            nav_button_element_second = nav_button_container.find_elements(By.XPATH, '//button[@class="css-bugrro-unf-pagination-item"]')
                            current_active_button = findActiveButtons(nav_button_element_second, 'data-active')
            else:
                # without pagination 
                
                detail_content = driver.page_source
                detail_soup_second = BeautifulSoup(detail_content, 'html.parser')
                current_rows_of_reviewers = detail_soup_second.find_all('article', class_='css-72zbc4')
                print('without pagination_lenght', len(current_rows_of_reviewers))
                no_pagination_review_count = 0
                no_pagination_review_count_per_page = 0

                for review in current_rows_of_reviewers:
                    customer_name = review.find('span', class_='name').text
                    customer_review_container = review.find('p', class_='css-ed1s1j-unf-heading e1qvo2ff8')
                    customer_review = customer_review_container.find('span').text if customer_review_container else ''

                    customer_review_item = {
                        'customer_name': customer_name,
                        'customer_review': customer_review
                    }

                    review_list.append(customer_review_item)

                    no_pagination_review_count += 1
                    no_pagination_review_count_per_page += 1
                    print('reviewList without pagination', customer_review_item)
                return review_list
    else:
        # empty comments
        return review_list
                


def getSellerDetail(driver):
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1wbjdax')))
    print('seller detail executed')
    detail_content = driver.page_source
    detail_soup = BeautifulSoup(detail_content, 'html.parser')
    
    # seller_name = detail_soup.find('div', class_='css-k008qs')
    # print('seller_name', seller_name)
    detail_soup = BeautifulSoup(detail_content, 'html.parser')
    seller_name = detail_soup.find('h2', class_='css-1wdzqxj-unf-heading e1qvo2ff2').text 
    print('seller_name', seller_name)
    seller_performance = detail_soup.find_all('div', class_='css-1h5fp8g')
    seller_responsiveness = seller_performance[1].find('span').text
    seller_rate = seller_performance[0].find('span').text
    seller_location_element = detail_soup.find('h2', class_='css-1pd07ge-unf-heading e1qvo2ff2')
    seller_location = seller_location_element.find('b').text
    seller_category = driver.find_element(by=By.CLASS_NAME, value='css-ebxddb').get_attribute('alt')
    print('seller_category', seller_category)

    seler_section = {
        'seller_name' : seller_name,
        'seller_responsiveness': seller_responsiveness,
        'seller_rate': seller_rate,
        'seller_category': seller_category,
        'seller_location': seller_location
    }
    return seler_section

def getProductDetail(driver):
    detail_content = driver.page_source
    detail_soup = BeautifulSoup(detail_content, 'html.parser')
    time.sleep(10)
    PRODUCT_DETAIL = {}
    wait = WebDriverWait(driver, 30)

    #__PRODUCT SECTION
    product_name = detail_soup.find('h1', class_='css-1os9jjn').text
    product_category = detail_soup.find_all('li', class_='css-d5bnys')
    product_category_index = product_category[1].text
    
    product_price_container = detail_soup.find('div', class_='css-chstwd')
    product_original_price = product_price_container.find('div', class_='original-price').text if(product_price_container.find('div', class_='original-price')) else ''
    product_price = product_price_container.find('div', class_='price').text
    
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-bczdt6')))
    quantity_of_sold_product_container = detail_soup.find('div', class_='css-bczdt6')
    print('quantity_of_sold_product_container', quantity_of_sold_product_container)
    print('get_sold_prodct_array', detail_soup.find_all('p', class_='css-vni7t6-unf-heading e1qvo2ff8'))
    quantity_of_product_sold = quantity_of_sold_product_container.find('p', class_='css-vni7t6-unf-heading e1qvo2ff8')
    print('quantity_of_product_sold', quantity_of_product_sold)
    get_quanity_of_product_sold = quantity_of_product_sold.text if quantity_of_product_sold else ''
    
    product_detail = {
        'product_name': product_name,
        'product_category_index': product_category_index,
        **({'product_original_price': product_original_price} if product_original_price else {}),
        'product_sold_quantity': get_quanity_of_product_sold if get_quanity_of_product_sold else '',
        'product_price': product_price
    }

    print('product_detail', product_detail)
    # UPDATE-PRODUCT-SECTION #
    PRODUCT_DETAIL.update(product_detail)

    print('PRODUCT_DETAIL',PRODUCT_DETAIL)
    
    #__SELLER SECTION
    
    scroll_height = 500
    driver.execute_script(f"window.scrollBy(0, {scroll_height});")
    print('scrolled')
    time.sleep(10)
    
    SELLER_DETAIL = getSellerDetail(driver)
    print('seller detail collected')
    # UPDATE-SELLER-SECTION #
    PRODUCT_DETAIL.update(SELLER_DETAIL)
    print('product detail collected')

    #__CUSTOMER REVIEW SECTION
    scroll_height2 = 1000
    driver.execute_script(f"window.scrollBy(0, {scroll_height2});")
    
    REVIEW_DETAIL = getReviewDetail(driver)
    # UPDATE-REVIEW_DETAIL-SECTION #
    print_message(f'REVIEW_DETAIL {REVIEW_DETAIL}', 'info', True)
    print_message(f'PRODUCT_DETAIL_SECTION {PRODUCT_DETAIL}', 'info', True )
    PRODUCT_DETAIL_RESULT = {}
    if len(REVIEW_DETAIL) > 0:
        PRODUCT_DETAIL['customer_reviews'] = REVIEW_DETAIL
        PRODUCT_DETAIL_RESULT['result'] = flattenCustomerReviews(PRODUCT_DETAIL, 'customer_reviews', 'customer_name', 'customer_review')
    else:
        PRODUCT_DETAIL.update({'customer_name': '', 'customer_review': ''})
    print_message(f'PRODUCT_DETAIL_RESULT {PRODUCT_DETAIL_RESULT}', 'info', True)
    return PRODUCT_DETAIL_RESULT['result'] if PRODUCT_DETAIL_RESULT else PRODUCT_DETAIL