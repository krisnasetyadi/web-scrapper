from main_functions.main_srape_function import scrapeTokopediaData
from utils.helpers import print_message
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException

retry_count = 0
MAX_RETRY = 10

while retry_count < MAX_RETRY:
    try:
        scrapeTokopediaData()
        break
    except TimeoutException:
        print_message(f"TimeoutException occurred in main function (retry {retry_count + 1}/{MAX_RETRY}), retrying in 10 seconds...", 'warning')
        time.sleep(10)
        retry_count += 1
    except NoSuchElementException:
        print_message(f"NoSuchElementException occurred  in main function (retry {retry_count + 1}/{MAX_RETRY}), retrying in 10 seconds...", 'warning')
        time.sleep(10)
        retry_count += 1
else:
    print_message(f'Max retries reached {MAX_RETRY}. exiting...', 'danger', bold=True)
