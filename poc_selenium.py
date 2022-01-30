from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time


def submit_guess(word_content):
    driver=webdriver.Firefox(executable_path="C:\Python\geckodriver\geckodriver.exe")
    driver.get("https://term.ooo")
    assert "Termo" in driver.title
    time.sleep(2)
    
    help_modal = driver.find_element_by_id('helpclose')
    help_modal.click()
    time.sleep(2)

    for letter in word_content:
        letter_key = driver.find_element_by_id(f'kbd_{letter}')
        letter_key.click()
        time.sleep(1)
                
    enter_key = driver.find_element_by_id('kbd_enter')
    enter_key.click()
    
    time.sleep(2)        
    driver.close()        
        

submit_guess('feliz')