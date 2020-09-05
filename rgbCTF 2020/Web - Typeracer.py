from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

URL = "http://167.172.123.213:8973/"

# Using chromedriver 83.0.4103
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(URL)

STARTCHAL = WebDriverWait(driver, 10).until(
	EC.visibility_of_element_located((By.XPATH, "//a[@class='btn btn-outline-dark mt-3']"))
	)

STARTCHAL.click()

# Wait for time taken to start counting i.e. for words to start appearing on screen
try:
	WebDriverWait(driver, 90000).until_not(
		EC.text_to_be_present_in_element((By.ID, 'timetaken'), "0")
	)
except:
	pass


driver.execute_script("document.querySelector('textarea').removeAttribute('disabled')")


words = {}
s = BeautifulSoup(driver.page_source, 'html.parser')
for span in s.find("div", {"class": "card-body"}).findAll("span", recursive=False):
	order = span.attrs['style'].split(';')[0].split(':')[-1].strip()
	words[int(order)] = span.text.strip('\xa0')

orderedWords = OrderedDict(sorted(words.items()))
complete = " ".join([word for order, word in orderedWords.items()])
textbox = driver.find_element_by_xpath("//textarea")
textbox.send_keys(complete)
