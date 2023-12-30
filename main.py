from main_functions.main_srape_function import scrapeTokopediaData
from utils.helpers import print_message, storingLoggingAs, playSoundWithStatus, scrollFromToptoBottom
import time
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.product_list_helpers import getTotalPaginationAndExtractUrl
import concurrent.futures
from config.config_parameters import BASE_SEARCH_URL_PARAMETER
import threading 
# Set the maximum number of concurrent drivers
MAX_CONCURRENT_DRIVERS = 5
MAX_CONCURRENT_WINDOWS = 2
driver_semaphore = threading.Semaphore(MAX_CONCURRENT_DRIVERS)
windows_semaphore = threading.Semaphore(MAX_CONCURRENT_WINDOWS)

retry_count = 0
MAX_RETRY = 10
# START 11.35 5 DRIVER
def runSrapper(url):
       with driver_semaphore:
        try:
            with windows_semaphore:
            # Your existing scraping logic here
                scrapeTokopediaData(url)
        except Exception as e:
            print_message(f'Error during scraping: {e}', 'error')
            playSoundWithStatus('error', 4)

if __name__ == '__main__':
    while retry_count < MAX_RETRY:
        try:
            ua = UserAgent()
            uc_chrome_options = uc.ChromeOptions()
            uc_chrome_options.add_argument(f'user-agent={ua.random}')
            uc_chrome_options.add_argument('--disable-popup-blocking')
            driver = uc.Chrome(options=uc_chrome_options, use_subprocess=False)
            print('driver setup on main func ...')
            driver.get(BASE_SEARCH_URL_PARAMETER)
            storingLoggingAs('info', 'run driver and sleep for 30 seconds...')
            time.sleep(30)
            FOOTER_CLASS = 'css-dmrkw7'
            
            [scrolled] = scrollFromToptoBottom(driver, f'{FOOTER_CLASS}', False, True, 10)
            print('scrolled to footer in main func', scrolled)
            
            [urls_and_pagination, total_pagination] = getTotalPaginationAndExtractUrl(driver)
            print('urls_and_pagination', urls_and_pagination)
            time.sleep(10)
            if len(urls_and_pagination) > 0 and scrolled:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(runSrapper, url) for url in urls_and_pagination]
                    concurrent.futures.wait(futures)
                # scrapeTokopediaData()
                # break
        except TimeoutException:
            print_message(f"TimeoutException occurred in main function (retry {retry_count + 1}/{MAX_RETRY}), retrying in 10 seconds...", 'warning')
            time.sleep(10)
            retry_count += 1
        except NoSuchElementException:
            print_message(f"NoSuchElementException occurred  in main function (retry {retry_count + 1}/{MAX_RETRY}), retrying in 10 seconds...", 'warning')
            time.sleep(10)
            retry_count += 1
        except Exception as e:
            print_message(f'main error message {e}', 'error')
            playSoundWithStatus('error', 4)
    else:
        print_message(f'Max retries reached {MAX_RETRY}. exiting...', 'danger', bold=True)
