from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time 

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


def scrollFromToptoBottom(dvr, boundary_component, byId=False, no_scroll_top=False):
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
            time.sleep(5)
        
    if is_boundary_component or scroll_count == timeout_scroll and not no_scroll_top:
        dvr.execute_script("window.scrollTo(0, 0);")
        return [True]
    if is_boundary_component or scroll_count == timeout_scroll and no_scroll_top:
        return [True]
    else:
        return [False]
    
def findActiveButtons(array, attr):
    for item in array:
        if item is not None:
            if attr and item.get_attribute(attr) == 'true':
                return item.text
        return None
    