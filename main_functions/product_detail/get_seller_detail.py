from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from utils.helpers import storingLoggingAs

def getSellerDetail(driver):
    storingLoggingAs('info', 'seller detail executed...')
    detail_content = driver.page_source
    detail_soup = BeautifulSoup(detail_content, 'html.parser')
    seller_name = detail_soup.find('h2', class_='css-1wdzqxj-unf-heading e1qvo2ff2').text 
    seller_performance = detail_soup.find_all('div', class_='css-1h5fp8g')
    seller_responsiveness = seller_performance[1].find('span').text
    seller_rate = seller_performance[0].find('span').text
    seller_location_element = detail_soup.find('h2', class_='css-1pd07ge-unf-heading e1qvo2ff2')
    seller_location = ''
    if seller_location_element is not None:
        seller_location = seller_location_element.find('b').text
    seller_category = driver.find_element(by=By.CLASS_NAME, value='css-ebxddb').get_attribute('alt')
    seller_star_percentage_paragraph = detail_soup.find('p', class_='css-g3cl0z-unf-heading e1qvo2ff8')
    seller_star_percentage = f"{seller_star_percentage_paragraph.find('span').text.split('%')[0]}%" if seller_star_percentage_paragraph is not None else ''

    seler_section = {
        'seller_name' : seller_name,
        'seller_responsiveness': seller_responsiveness,
        'seller_rate': seller_rate,
        'seller_star_percentage': seller_star_percentage if seller_star_percentage else '',
        'seller_category': seller_category,
        'seller_location': seller_location,
    }
    return seler_section