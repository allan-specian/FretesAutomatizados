# packages: selenium, webdriver_manager, time, pandas

import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from Package import Package

service = Service(ChromeDriverManager().install())  # automatizar instalação do chromedriver
driver = webdriver.Chrome(service=service)

package = Package("5", "15", "17", "0.3", "32.5")
backspace = '\b\b\b'

driver.get("https://melhorenvio.com.br")
driver.find_element('xpath', '//*[@id="from"]').send_keys('03071050')
driver.find_element('xpath', '//*[@id="to"]').send_keys('13560544')
driver.find_element(By.ID, 'height').send_keys(backspace + package.get_height())
driver.find_element('xpath', '//*[@id="width"]').send_keys(backspace + package.get_width())
driver.find_element('xpath', '//*[@id="length"]').send_keys(backspace + package.get_length())
driver.find_element('xpath', '//*[@id="weight"]').send_keys(backspace + package.get_weight())
driver.find_element('xpath', '//*[@id="insuranceValue"]').send_keys(backspace + package.get_price())

# Necessario aceitar os cookies para poder clicar no botao de calular
driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[1]/button').click()
time.sleep(4)  # seconds
driver.find_element(By.ID, "calculate").click()
time.sleep(3)

elemento = driver.find_element(By.XPATH, '//*[@id="calculator"]/div/div[1]/div[1]/table')
html_tabela = elemento.get_attribute('outerHTML')

# Usando regex
# Delete all <div>, </div>, <a> and </a> tags
html_tabela = re.sub(r'</?div[^>]*>', '', html_tabela)
html_tabela = re.sub(r'</?a[^>]*>', '', html_tabela)
# Replace <img> tags with the content of their alt attribute
html_tabela = re.sub(r'<img[^>]*alt="([^"]*)"[^>]*>', r'\1', html_tabela)

dfs = pd.read_html(html_tabela)
df = dfs[0]
df = df.drop(df.columns[5], axis=1)  # deletar a ultima coluna, um link de cadastrar/imagem de seta
print(html_tabela)
print(dfs)
count = 0

df.to_excel('output.xlsx', index=False)
driver.close()
