from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep

# Entrar no site do SGP: https://ralpnet.sgp.net.br/accounts/login

driver = webdriver.Firefox()
driver.get('https://ralpnet.sgp.net.br/accounts/login')
sleep(1)

# Digitar usuário e senha

campo_usuario = driver.find_element(By.XPATH,"//input[@id='id_username']")
campo_senha = driver.find_element(By.XPATH,"//input[@id='inlineFormInputGroup']")

campo_usuario.send_keys('usuario')  # Inserir o nome de usuário
sleep(1) 
campo_senha.send_keys('senha')  # Inserir a senha
sleep(1)

# Enviar formulário
campo_senha.send_keys(Keys.RETURN)
