from selenium.webdriver.common.by import By

def handleReviewCategory(driver):
    find_accordion_container = driver.find_elements(By.XPATH, '//div[@class="css-1i5ul9s-unf-accordion eqwvqlj4"]')
    find_accordion = find_accordion_container[2].find_element(By.XPATH, '//button[@class="css-ll75b2-unf-accordion__header"]')
    is_accordion_expanded = find_accordion.get_attribute('aria-expanded')
    print('is_accordion_expanded', is_accordion_expanded)
    status = ''
    if is_accordion_expanded is True:
        status = 'checkbox_ready'
    else:
        find_accordion[2].click()
        status = 'is_clicked'
    # unf-accordion__content-wrapper

    if 'checkbox_ready' in status:
        find_accordion_container = driver.find_elements(By.XPATH, '//div[@class="css-1i5ul9s-unf-accordion eqwvqlj4"]')
        renderred_checkboxs_container = find_accordion_container[2].find_elements(By.XPATH, '//div[@class="css-8wwjx7-unf-checkbox e4ba57s3"]')
        for renderred_checkbox in renderred_checkboxs_container:
            renderred_checkbox
    # css-1xdqrvt eqwvqlj1
    # css-8wwjx7-unf-checkbox e4ba57s3
   
    
