import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException

driver = webdriver.Chrome()
driver.get("https://monkeytype.com/")
time.sleep(2)

try:
    accept_button = driver.find_element(By.CSS_SELECTOR, "button.acceptAll")
    accept_button.click()
    time.sleep(1)
except NoSuchElementException:
    pass

input_field = driver.find_element(By.ID, "wordsInput")
driver.execute_script("arguments[0].focus();", input_field)
words_div = driver.find_element(By.ID, "words")

try:
    word_elements = words_div.find_elements(By.CLASS_NAME, "word")
    if word_elements:
        first_word_elem = word_elements[0]
        letters = first_word_elem.find_elements(By.TAG_NAME, "letter")
        if letters:
            first_letter = letters[0].text
            input_field.send_keys(first_letter)
except Exception:
    pass

while True:
    time_left = 30
    try:
        time_elem = driver.find_element(By.CSS_SELECTOR, "#liveStatsMini .time")
        if time_elem is not None:
            classes = time_elem.get_attribute("class")
            text = time_elem.text.strip()
            if "hidden" not in classes and text:
                time_left = int(text)
    except (NoSuchElementException, ValueError, StaleElementReferenceException):
        pass

    if time_left <= 0:
        break

    try:
        active_word = driver.find_element(By.CLASS_NAME, "word.active")
        driver.execute_script(
            "arguments[0].style.border = '2px solid yellow'; "
            "arguments[0].style.borderRadius = '50%';",
            active_word
        )
        letters = active_word.find_elements(By.TAG_NAME, "letter")
        current_word = "".join([letter.text for letter in letters])
        if current_word:
            input_field.send_keys(current_word + " ")
    except (NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException):
        break

time.sleep(2)

driver.save_screenshot("x.png")

import os
os.startfile("x.png")
driver.quit()