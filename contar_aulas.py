
# Just a module to hold my credetials
import qsettings
import os, sys
import json
import msvcrt
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


url = 'https://qacademico.ifce.edu.br/qacademico/index.asp?t=1000'

# Domínio
qAcad = {
    'N_ETAPA': ['1B', '2B', 'PF'],
    'COD_PAUTA': [329829, 32981, 329792],
    'MODO':['FALTAS', 'AULAS'],
    't':[3066]

}

'''
IE:
https://qacademico.ifce.edu.br/qacademico/index.asp?t=3066&MODO=FALTAS&&ETAPA=1&=1B#
https://qacademico.ifce.edu.br/qacademico/index.asp?t=3066&MODO=FALTAS&COD_PAUTA=329829&ETAPA=2&N_ETAPA=2B#

https://qacademico.ifce.edu.br/qacademico/index.asp?t=3068&COD_PAUTA=329829&ETAPA=1&N_ETAPA=1B
https://qacademico.ifce.edu.br/qacademico/index.asp?t=3068&COD_PAUTA=329829&ETAPA=2&N_ETAPA=2B
https://qacademico.ifce.edu.br/qacademico/index.asp?t=3068&COD_PAUTA=329829&ETAPA=9&N_ETAPA=PF

IA:
https://qacademico.ifce.edu.br/qacademico/index.asp?t=3066&MODO=FALTAS&COD_PAUTA=329819&ETAPA=1&N_ETAPA=1B#

IP:
https://qacademico.ifce.edu.br/qacademico/index.asp?t=3066&MODO=FALTAS&COD_PAUTA=329792&ETAPA=1&N_ETAPA=1B#

'''

debug = False

# create a output folder
output_folder = 'screens'
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

# download the chrome driver from
# https://sites.google.com/a/chromium.org/chromedriver/downloads
# and put it in the current directory
chrome_driver = os.path.join(os.getcwd(), "drivers/chromedriver{}".format('.exe' if sys.platform == 'win32' else ''))

print('Plataform', sys.platform)

if not debug:
    print('Create a Headless Chrome Webdriver..')
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
else:
    driver = webdriver.Chrome(executable_path=chrome_driver)



print('Go to URL...')
driver.get(url)

print('Filling the login form')
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'LOGIN')))
driver.find_element_by_name('LOGIN').send_keys(qsettings.username)
driver.find_element_by_name('SENHA').send_keys(qsettings.password)

print('Try to access the system..')
driver.find_element_by_id('btnOk').click()

# capture the start screen
driver.get_screenshot_as_file(os.path.join(output_folder, "screen01.png"))

# Link "Meus Diários"
next_page = 'https://qacademico.ifce.edu.br/qacademico/index.asp?t=3061'
driver.get(next_page)

# Link 
next_page = "https://qacademico.ifce.edu.br/qacademico/index.asp?t=3066&COD_PAUTA=329792&N_ETAPA=2B&MODO="
driver.get(next_page)

# Scraping now
ch_sum = 0
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('table', {'class':'conteudoTexto'})
for tr in table.findAll('tr')[2:-1]:
    tds = tr.findAll('td')
    if len(tds) == 4:
        tag_pre__contents = tds[1].find('pre').contents
        tt_aula = tag_pre__contents[0] if len(tag_pre__contents) > 0 else ''
        ch_aula = tds[2].contents[0]
        if tt_aula.replace(' ', '') != '':
            ch_sum += int(ch_aula)

print('ch sum:', ch_sum)

print('Press Enter to finish..')
msvcrt.getch()

# Finally, closes the browser
driver.close()
