
# Just a module to hold my credetials
import qsettings
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

# download the chrome driver from
# https://sites.google.com/a/chromium.org/chromedriver/downloads
# and put it in the current directory
chrome_driver = os.path.join(os.getcwd(), "drivers/chromedriver")

print('Create a Headless Chrome Webdriver..')
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)


print('Go to URL...')
driver.get(qsettings.url)

print('Filling the login form')
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'LOGIN')))
driver.find_element_by_name('LOGIN').send_keys(qsettings.username)
driver.find_element_by_name('SENHA').send_keys(qsettings.password)

print('Try to access the system..')
driver.find_element_by_id('btnOk').click()

# capture the start screen
driver.get_screenshot_as_file("screen01.png")

# Finally, closes the browser
driver.close()

print('End!')
