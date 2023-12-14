from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import extractHrefParameter

def getAllURLPerPage(driver):
    redirect_urls = []
    wait = WebDriverWait(driver, 120)
    
    all_item_each_page = driver.find_elements(By.XPATH, '//div[@class="css-19oqosi"]')
    total_item_per_page = len(all_item_each_page)
    for item_index in range(int(total_item_per_page)):
        list_item_each_page = driver.find_elements(By.XPATH, '//div[@class="css-19oqosi"]')
        item = list_item_each_page[item_index]
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        anchor = item.find_element(By.TAG_NAME, 'a')
        href = anchor.get_attribute('href')
        url = extractHrefParameter(href)
        redirect_urls.append(url)
    print('redirect_urls', redirect_urls)
    return redirect_urls