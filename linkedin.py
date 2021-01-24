import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def initial_setup():
    #Creo el driver de firefox
    driver = webdriver.Firefox()
    #Dirijo a web de linkedin
    driver.get("https://www.linkedin.com")
    #deserializo las cookies,que se deben encontrar en el directorio raíz
    cookies = pickle.load(open("cookies.pkl", "rb"))
    #cargo las cookies de sesión
    for cookie in cookies:
        driver.add_cookie(cookie)
    #actualizo la página
    driver.get("http://www.linkedin.com")

#lanzo el metodo de configuración inicial
initial_setup()



