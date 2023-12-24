
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

from utils.helpers import storingLoggingAs

def getReviewDetail(driver):
    print('processing review section . . .')
    
    time.sleep(60)
    detail_content = driver.page_source
    detail_soup = BeautifulSoup(detail_content, 'html.parser')
    total_reviews_element = detail_soup.find('p', class_='css-e84n4s-unf-heading e1qvo2ff8')
    current_rows_of_reviewers = detail_soup.find_all('article', class_='css-72zbc4')
    total_rows_per_page = len(current_rows_of_reviewers)
    print('total_rows_per_page', total_rows_per_page)
    print('current_rows_of_reviewers', current_rows_of_reviewers)

    MAX_BUTTON_PER_NAV = 9

    # there's some reviews
    if len(current_rows_of_reviewers) > 0:
        review_list = []

        total_review_string = total_reviews_element.text
        total_review = total_review_string.split()[3] if total_review_string else None
        storingLoggingAs('info', f'total reviews: {total_review}')
        # logging.info(f'total reviews: {total_review}')
        
        if total_review is not None:
            FIND_REVIEW_PAGE_CONTROLLER = detail_soup.find('div', class_='css-1xqkwi8')

            navigation_controller = ''
            if FIND_REVIEW_PAGE_CONTROLLER:
                navigation_controller = detail_soup.find('nav', class_='css-txlndr-unf-pagination')
            else:
                navigation_controller = None

            if navigation_controller is not None:
                # has pagination
                nav_button_container = driver.find_element(By.XPATH, '//div[@class="css-1xqkwi8"]')
                nav_button_element = nav_button_container.find_elements(By.XPATH, '//button[@class="css-bugrro-unf-pagination-item"]')
                last_pagination_button = nav_button_element[MAX_BUTTON_PER_NAV - 1].text if len(nav_button_element) == MAX_BUTTON_PER_NAV  else nav_button_element[len(nav_button_element) - 1].text

                storingLoggingAs('info', f'total pagination: {int(last_pagination_button)}')
                for i in range(int(last_pagination_button)):
                    storingLoggingAs('info', f'processing of {i} pagination with total rows per page: {total_rows_per_page}')

                    with_pagination_review_count = 0
                    with_pagination_review_count_per_page = 0

                    nav_button_container = driver.find_element(By.XPATH, '//div[@class="css-1xqkwi8"]')
                    nav_button_element = nav_button_container.find_elements(By.XPATH, '//button[@class="css-bugrro-unf-pagination-item"]')
             
                    # current_active_button = findActiveButtons(nav_button_element, 'data-active')

                    for review_index in range(total_rows_per_page):
                        customer_name = current_rows_of_reviewers[review_index].find('span', class_='name').text
                        customer_review_container = current_rows_of_reviewers[review_index].find('p', class_='css-ed1s1j-unf-heading e1qvo2ff8')
                        customer_review = customer_review_container.find('span').text if customer_review_container else ''

                        customer_review_item = {
                            'customer_name': customer_name,
                            'customer_review': customer_review
                        }

                        review_list.append(customer_review_item)
                        with_pagination_review_count += 1
                        with_pagination_review_count_per_page += 1

                    if with_pagination_review_count_per_page == total_rows_per_page:
                        storingLoggingAs('info', 'processing reviews with pagination...')
                        # why CLASS_NAME "css-bugrro-unf-pagination-item" declare twice ? to always refresh /fetch the element
                        nav_button_container_second = driver.find_element(By.XPATH, '//div[@class="css-1xqkwi8"]')
                        time.sleep(2)
                        next_element = nav_button_container_second.find_elements(By.XPATH, '//button[@class="css-16uzo3v-unf-pagination-item"]')[1]
                        next_element_aria_label = next_element.get_attribute('aria-label')
                        next_element_is_disabled = next_element.get_attribute('disabled')

                        if next_element_aria_label == 'Laman berikutnya'and next_element_is_disabled:
                            return review_list
                        
                        if next_element_aria_label == 'Laman berikutnya' and (not next_element_is_disabled or next_element_is_disabled is None):
                            next_element.click()
                            storingLoggingAs('info', 'next button clicked.')
                            next_element = nav_button_container_second.find_elements(By.XPATH, '//button[@class="css-16uzo3v-unf-pagination-item"]')[1]
                            next_element_aria_label = next_element.get_attribute('aria-label')
                            next_element_is_disabled = next_element.get_attribute('disabled')

                            # reset the value and click
                            with_pagination_review_count_per_page = 0

                            time.sleep(5)

                            # Fetch the new set of current_rows_of_reviewers
                            next_element = nav_button_container_second.find_elements(By.XPATH, '//button[@class="css-16uzo3v-unf-pagination-item"]')[1]
                            detail_content = driver.page_source
                            detail_soup_second = BeautifulSoup(detail_content, 'html.parser')

                            current_rows_of_reviewers = detail_soup_second.find_all('article', class_='css-72zbc4')
                            total_rows_per_page = len(current_rows_of_reviewers)
                            storingLoggingAs('info', 'resetting value after clicked.')
                return review_list
            else:
                # without pagination 
        
                detail_content = driver.page_source
                detail_soup_second = BeautifulSoup(detail_content, 'html.parser')
                current_rows_of_reviewers = detail_soup_second.find_all('article', class_='css-72zbc4')
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
                storingLoggingAs('info', f'without pagination {review_list}')
                return review_list
    else:
        # empty comments
        print('get_empty_comments')
        return []