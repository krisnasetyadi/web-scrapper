from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import logging

from datetime import datetime
import pandas as pd
import pygame
import time 
import os
import sys

from urllib.parse import unquote, urlparse, parse_qs

def print_message(text, color, bold=False):
    color_code = ''
    if color == 'danger':
        color_code = "\033[91m"
    elif color == 'success':
        color_code = "\033[92m" 
    elif color == 'info':
        color_code = "\033[94m"
    elif color == 'warning':
        color_code = "\033[93m"
    
    if bold == True:
        return print(f"{color_code}\033[1m{text}\033[0m")
    else:
        return print(f"{color_code}{text}\033[0m")


def scrollFromToptoBottom(dvr, boundary_component, byId=False, no_scroll_top=False, sleepTime = 5):
    scrolled = False
    timeout_scroll = 30
    scroll_count = 0
    is_boundary_component = False
    
    print_message(f'scrolling . . . {boundary_component}', 'info')

    while not scrolled and scroll_count < timeout_scroll and not is_boundary_component: 
        current_scroll_position = dvr.execute_script("return window.pageYOffset;")
        document_height = dvr.execute_script("return document.documentElement.scrollHeight;")
        print('current_scroll_position', current_scroll_position)
        print('document_height', document_height)
        try:
            boundary_element = dvr.find_element(by=By.CLASS_NAME, value=f'{boundary_component}') if not byId else dvr.find_element(by=By.ID, value=f'{boundary_component}')  
            if boundary_element:
                scrolled = True
                is_boundary_component = True
        except NoSuchElementException:
            scrolled = False
            is_boundary_component = False
            scroll_height = 500
            dvr.execute_script(f"window.scrollBy(0, {scroll_height});")
            scroll_count += 1
            print('scroll_count', scroll_count)
            time.sleep(sleepTime)
        
    if no_scroll_top == False:
        if scroll_count == timeout_scroll or is_boundary_component:
            print('get_this_func_1')
            dvr.execute_script("window.scrollTo(0, 0);")
            return [True]
        
    if no_scroll_top == True:
        if is_boundary_component or scroll_count == timeout_scroll:
            print('get_this_func_2')
            return [True]
    else:
        return [False]
    
def findActiveButtons(array, attr):
    for item in array:
        if item is not None:
            if attr and item.get_attribute(attr) == 'true':
                return item.text
        return None

def flattenCustomerReviews(data, key1='', key2='', key3=''):
    flattened_data = []
    for item in [data]:
        for review in item[key1]:
            flattened_item = item.copy()
            flattened_item[key2] = review[key2]
            flattened_item[key3] = review[key3]
            del flattened_item[key1]
            flattened_data.append(flattened_item)
    return flattened_data


def extractHrefParameter(url = ''):
    # check if the url have redirect parameter
    if 'r=https' in url:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        r_parameter_value = query_params.get('r', [])[0]
        decoded_r_value = unquote(r_parameter_value)
        return decoded_r_value
    else:
        return url

def saveToCSV(array=[], keyword='', status='', optionalText=''):
    current_datetime = datetime.now()
    formatted_timestamp = current_datetime.strftime("%Y%m%d%H%M%S")
    
    storing = []
    if len(array) > 0:
        isArrayOfObject = False
        for i in array:
            if isinstance(i, list):
                storing.extend(i)
            elif isinstance(i, dict):
                isArrayOfObject = True
                break
        if isArrayOfObject:
            storing = array

    storingLoggingAs('info', f'storing-stores {storing}')
    current_storing_size = sys.getsizeof(storing)
    current_array_size = sys.getsizeof(array)
    storingLoggingAs('warning', f'size_of_array {current_array_size} -- size_of_storing {current_storing_size}')
    
    if len(storing) > 0:
        df = pd.DataFrame(storing)
        df.index += 1
        df.index.rename('number', inplace=True)

        store_folder = 'csv_stores'

        os.makedirs(store_folder, exist_ok=True)

        success_folder = os.path.join(store_folder, 'success')
        error_folder = os.path.join(store_folder, 'error')
        each_product_folder = os.path.join(store_folder, 'each_product')

        os.makedirs(success_folder, exist_ok=True)
        os.makedirs(error_folder, exist_ok=True)
        os.makedirs(each_product_folder, exist_ok=True)

        file_path = ''

        if status == 'success':
            file_path = os.path.join(success_folder, f'product_{keyword}_{optionalText}{formatted_timestamp}.csv')
        if status == 'failed':
            file_path = os.path.join(error_folder, f'product_{keyword}_{optionalText}{formatted_timestamp}.csv')
        if status == 'success_each_item':
            file_path = os.path.join(each_product_folder, f'product_{keyword}_{optionalText}{formatted_timestamp}.csv')
            storing = []
        df.to_csv(file_path)
        playSoundWithStatus('success')

def storingLoggingAs(status='', text=''):
    current_date_time = datetime.now()
    formatted_date_time = current_date_time.strftime("%Y%m%d")

    level_logging = {
        'info': logging.INFO,
        'error': logging.ERROR, 
        'warning': logging.WARNING
    }

    logs_folder = 'logs'
    os.makedirs(logs_folder, exist_ok=True)
    
    log_file_path = os.path.join(logs_folder, f'scrapper_{formatted_date_time}.log')

    logger = logging.getLogger('logger') 
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(level_logging[status])
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    logger.log(level_logging[status], f'{text}')
    

def playSoundWithStatus(status='error', times=1):
    pygame.mixer.init()
   
    sound_by_status = pygame.mixer.Sound(f'./sound_assets/{"collierhs_colinlib__elevator_ding" if status == "error" else "glass_ping_Go445"}.wav')
   
    for i in range(times):
        sound_by_status.play()
        pygame.time.wait(int(sound_by_status.get_length() * 1000))


def extractCurrentUrlPage(url):
    return url.split('=')[1]